#-*- coding:utf-8 -*-
"""命令行解析模块"""

from requestreader import RequestReader
from xml.etree import ElementTree
from cmd import Cmd

class RequestCommand(Cmd):
    """命令解析工具类"""
    __SHOW_SUBCOMMAND = ['requests', 'projects']
    __PROCONF_SUBCOMMAND = ["on", "off", "status"]
    __storage = {}

    #---------------------------------------------------------------------------
    def __init__(self, xml_file_name):
        '''init'''
        Cmd.__init__(self)
        try:
            self.__request_urlreader = RequestReader(xml_file_name)
        except IOError:
            print "No such file: '%s'" % xml_file_name
            exit(1)
        except ElementTree.ParseError, err:
            print "xml error:", err
            exit(1)
        self.__projects_file = xml_file_name
        self.__request_projects = self.__get_projects()
        self.__current_project_info = {"current_index":None, \
                "current_name": None}
        self.__current_project = None
        self.__project_config = False
        self.prompt = ">>> "
        self.intro = "welcome to cronus request tool by:kiravinci"

    #---------------------------------------------------------------------------
    def __get_request_entrys(self):
        """获取当前项目下所有RequestEntry"""
        return self.__current_project.get_request_entrys()

    #---------------------------------------------------------------------------
    def __get_projects(self):
        '''获取所有项目'''
        return self.__request_urlreader.get_request_projects()

    #---------------------------------------------------------------------------
    def __use_project_index(self, project_index):
        """以项目索引选择项目"""
        try:
            project_index = int(project_index) - 1
            self.__current_project = self.__request_projects[project_index]
            self.__current_project_info["current_name"] = None
            self.__current_project_info["current_index"] = project_index + 1
            print "use project ok"
        except IndexError:
            print "project index out arange."
        except ValueError:
            print "project param error."

    #---------------------------------------------------------------------------
    def __use_project_name(self, project_name):
        """以项目名称选择项目"""
        if project_name is None:
            print "project name is None"
            return

        for project in self.__request_projects:
            if project.get_project_name() == project_name:
                self.__current_project = project
                self.__current_project_info["current_name"] = project_name
                self.__current_project_info["current_index"] = None
                print "use project ok."
                return
        print "no project is name: %s" % project_name

    #---------------------------------------------------------------------------
    def do_prompt(self, prompt):
        '''更改命令提示符命令'''
        self.prompt = prompt

    #---------------------------------------------------------------------------
    def do_proconf(self, param):
        '''项目配置'''
        def print_status():
            """输出项目配置状态"""
            print "project config status:", self.__project_config

        if param == "status":
            return print_status()
        if param == "on":
            self.__project_config = True
            return print_status()
        if param == "off":
            self.__project_config = False
            return print_status()

        print "error command param."

    #---------------------------------------------------------------------------
    def complete_proconf(self, text, line, begidx, endidx):
        '''proconf命令自动补全'''
        if not text:
            completions = self.__PROCONF_SUBCOMMAND[:]
        else:
            completions = [subcommand for subcommand in \
                    self.__PROCONF_SUBCOMMAND if subcommand.startswith(text)]

        return completions

    #---------------------------------------------------------------------------
    def do_show(self, params):
        '''显示项目/RequestEntry命令'''
        try:
            params = params.split()
            func = getattr(self, "show_" + params[0])
            func(params[1:])
        except AttributeError:
            print "command '%s' is exist." % params[0]
        except IndexError:
            print "less command param."

    #---------------------------------------------------------------------------
    def complete_show(self, text, line, begidx, endidx):
        '''show 命令自动补全'''
        if not text:
            completions = self.__SHOW_SUBCOMMAND[:]
        else:
            completions = [subcommand for subcommand in self.__SHOW_SUBCOMMAND \
                    if subcommand.startswith(text)]

        return completions

    #---------------------------------------------------------------------------
    def show_projects(self, params):
        '''显示所有项目'''
        if self.__request_projects is None:
            return
        for index, request_project in enumerate(self.__request_projects):
            print "| Index:", index + 1, "| Name: %s | Alias: %s |\
                    " % (request_project.get_project_name(),  \
                    request_project.get_project_alias())

    #---------------------------------------------------------------------------
    def do_use(self, params):
        '''选择request项目'''
        from shlex import split
        from argparse import ArgumentParser
        
        # 选项解析器
        parser = ArgumentParser(description="select project with index | name.")
        # 互斥选项组
        project_group = parser.add_mutually_exclusive_group(required=True)
        # 添加互斥选项
        project_group.add_argument("-i", "--index", action="store", \
                            dest="select_index", type=int, \
                            help="select project with index.")
        project_group.add_argument("-n", "--name", action="store", \
                            dest="select_name", \
                            help="select project with name.")
        
        # 解析选项
        result = parser.parse_args(split(params))
        
        # 根据选项执行相应的动作
        if result.select_index is not None:
            self.__use_project_index(result.select_index)
        else:
            self.__use_project_name(result.select_name)

    #---------------------------------------------------------------------------
    def show_requests(self, params):
        '''显示当前项目下所有request'''
        if self.__current_project is None:
            print "no project selected."
            return
        first_index = 0
        requests_limit = 10
        try:
            if params:
                params_length = len(params)
                if params_length == 1:
                    requests_limit = int(params[0])
                if params_length == 2:
                    first_index = int(params[0]) - 1
                    requests_limit = int(params[1])
        except ValueError:
            print "limit param error."
            return
        request_entrys = self.__get_request_entrys()[first_index:first_index \
                + requests_limit]
        for index, request_entry in enumerate(request_entrys):
            print index + first_index + 1, "--->", \
                    request_entry.get_name()
        requests_total = len(self.__get_request_entrys())
        requests_limit = requests_limit if requests_limit < requests_total \
                else requests_total
        print "%d/%d total" % (requests_limit, len(self.__get_request_entrys()))

    #---------------------------------------------------------------------------
    def __reload(self, file_name, is_loadapp):
        """重新载入程序"""
        try:
            self.__request_urlreader = RequestReader(file_name)
        except IOError:
            print "No such file: '%s'" % file_name
            return
        except ElementTree.ParseError, err:
            print "xml error:", err
            return

        self.__request_projects = self.__get_projects()
        if is_loadapp:
            self.__current_project = None
            self.__project_config = False
            print "app reload success."
        else:
            if self.__current_project_info["current_index"]:
                self.__use_project_index(\
                        self.__current_project_info["current_index"])
            else:
                self.__use_project_name(\
                        self.__current_project_info["current_name"])
            print "project reload success."
        self.__projects_file = file_name

    #---------------------------------------------------------------------------
    def do_switch(self, params):
        """项目配置文件切换命令"""
        if params is None or params == "":
            print "miss project xml file."
            return

        self.__reload(params, True)

    #---------------------------------------------------------------------------
    def do_reload(self, params):
        """重新载入程序"""
        from shlex import split
        from argparse import ArgumentParser

        parser = ArgumentParser()
        project_group = parser.add_mutually_exclusive_group()
        project_group.add_argument("-a", action="store_const", \
                            dest="reload_config", const=True)
        project_group.add_argument("-p", action="store_const", \
                            dest="reload_config", const=False)
        results = parser.parse_args(split(params))
        self.__reload(self.__projects_file, results.reload_config)

    #---------------------------------------------------------------------------
    @classmethod
    def do_exit(cls, param):
        '''退出程序命令'''
        return True

    #---------------------------------------------------------------------------
    @classmethod
    def do_quit(cls, param):
        '''退出程序命令'''
        return True

    #---------------------------------------------------------------------------
    @classmethod
    def do_eof(cls, params):
        '''退出程序命令'''
        return True

    #---------------------------------------------------------------------------
    def do_req(self, params):
        '''以RequestEntry请求命令'''
        from requestcmd import RequestCmd

        req_config = {}
        req_config["storage"] = RequestCommand.__storage
        req_config["current_project"] = self.__current_project
        req_config["project_config"] = self.__project_config
        req_config["request_entrys"] = self.__get_request_entrys()

        RequestCmd.req(req_config, params)
