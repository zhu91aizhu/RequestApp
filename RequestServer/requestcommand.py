#-*- coding:utf-8 -*-
"""命令行解析模块"""

from requestreader import RequestReader
from xml.etree import ElementTree
from cmd import Cmd

class RequestCommand(Cmd):
    """命令解析工具类"""
    __SHOW_SUBCOMMAND = ['requests', 'projects']
    __PROCONF_SUBCOMMAND = ["on", "off", "status"]

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
            print "| Index:", index + 1, "| Name: \
                    ", request_project.get_project_name(), "| Alias:" \
                    , request_project.get_project_alias(), "|"

    #---------------------------------------------------------------------------
    def do_use(self, params):
        '''选择request项目'''
        params = params.split()
        params_length = len(params)
        if params_length == 0:
            print "miss param."
            return
        if len(params) == 1:
            self.__use_project_index(params[0])
            return
        if len(params) == 2:
            if params[0] == "-i":
                self.__use_project_index(params[1])
                return
            if params[0] == "-n":
                self.__use_project_name(params[1])

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
    @classmethod
    def __argument_parser(cls, params):
        """解析参数"""
        from shlex import split
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("-a", action="store", dest="append_params")
        parser.add_argument("-r", "--replace", action="store", \
                dest="replace_params")
        parser.add_argument("-d", "--data", action="store_const", \
                dest="is_print", const=True)
        project_group = parser.add_mutually_exclusive_group()
        project_group.add_argument("-c", action="store_const", \
                            dest="project_config", const=True)
        project_group.add_argument("-C", action="store_const", \
                            dest="project_config", const=False)
        parser.add_argument("-i", "--index", action="store", required=True, \
                            dest="request_index", type=int)

        return parser.parse_args(split(params))

    #---------------------------------------------------------------------------
    @classmethod
    def __update_params(cls, results, request_entrys, request_index):
        """更新参数字典"""
        append_params = {}
        append_params_tmp = []
        if results.append_params is not None:
            append_params_tmp = results.append_params.replace(" ", \
                                                                "").split(",")
        for append_param_tmp in append_params_tmp:
            param_tmp = append_param_tmp.split(":")
            append_params[param_tmp[0]] = param_tmp[1]

        src_params = request_entrys[request_index].get_params()
        if src_params is None:
            src_params = {}

        return dict(src_params, **append_params)

    #---------------------------------------------------------------------------
    @classmethod
    def __replace_params(cls, src_params, replace_params):
        """替换请求参数"""
        if replace_params is None:
            return src_params

        # 将请求参数转换成列表
        params = replace_params.replace(" ", "").split(",")
        for param in params:
            data = param.split(":")
            if not src_params.has_key(data[0]):
                print "replace param '%s' is not exists." % data[0]
                continue
            src_params[data[0]] = data[1]

        return src_params

    #---------------------------------------------------------------------------
    @classmethod
    def __print_params(cls, is_print, params):
        """打印参数"""
        import urllib

        if is_print is not None:
            print urllib.unquote_plus(params)

    #---------------------------------------------------------------------------
    def do_req(self, params):
        '''以RequestEntry请求命令'''
        import urllib
        import urllib2
        from json import dumps

        use_project_config = self.__project_config

        if self.__current_project is None:
            print "no project selected."
            return

        results = RequestCommand.__argument_parser(params)
        request_index = results.request_index - 1
        if results.project_config is not None:
            use_project_config = results.project_config

        try:
            request_entrys = self.__get_request_entrys()
            if use_project_config:
                url = self.__current_project.get_project_host() + ":" \
                        + self.__current_project.get_project_port() \
                        + "/" + request_entrys[request_index].get_url()
            else:
                url = request_entrys[request_index].get_url()

            # 更新请求参数
            request_params = RequestCommand.__update_params(results, \
                    request_entrys, request_index)
            # 替换请求参数
            request_params = RequestCommand.__replace_params(request_params, \
                    results.replace_params)
            # 转换请求参数
            request_params = urllib.urlencode({
                'data':dumps(request_params)})
            # 打印参数
            RequestCommand.__print_params(results.is_print, request_params)

            try:
                response = urllib2.urlopen(urllib2.Request(url, request_params))
                result = unicode(response.read(), 'utf-8')
                print result
            except ValueError as value_error:
                print "cannot access url or url error.", value_error
        except IndexError:
            print "req index error."
        except ValueError as value_error:
            print "limit param error.", value_error
        except urllib2.URLError as url_error:
            print "cannot access url or url error.", url_error
