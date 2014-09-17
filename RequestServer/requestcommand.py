#-*- coding:utf-8 -*-

import urllib
import urllib2
import json
from requestreader import RequestReader
from cmd import Cmd

class RequestCommand(Cmd):
    __SHOW_SUBCOMMAND = ['requests', 'projects']
    __PROCONF_SUBCOMMAND = ["on", "off", "status"]
    
    #-------------------------------------------------------------------------------
    def __init__(self, xmlfile):
        '''init'''
        Cmd.__init__(self)
        self.__reqUrlReader = RequestReader(r"requesturl.xml")
        self.__requestProjects = self.__getRequestProjects()
        self.__currentRequestProject = None
        self.__project_config = False
        self.prompt = ">>> "
        self.intro = "welcome to cronus request tool by:kiravinci"
        
    #-------------------------------------------------------------------------------
    def __getRequestEntrys(self):
        '''获取当前项目下所有RequestEntry'''
        return self.__currentRequestProject.getRequestEntrys()
    
    #-------------------------------------------------------------------------------
    def __getRequestProjects(self):
        '''获取所有项目'''
        return self.__reqUrlReader.getRequestProjects()
    
    #-------------------------------------------------------------------------------
    def __use_project_index(self, project_index):
        """以项目索引选择项目"""
        try:
            project_index = int(project_index) - 1
            self.__currentRequestProject = self.__requestProjects[project_index]
            print "use project ok"
        except IndexError:
            print "project index out arange."
        except ValueError:
            print "project param error."
    
    #-------------------------------------------------------------------------------
    def __use_project_name(self, project_name):
        """以项目名称选择项目"""
        for project in self.__requestProjects:
            if project.getProjectName() == project_name:
                self.__currentRequestProject = project
                print "use project ok."
                return
        print "no project is name: %s" % project_name
    
    #-------------------------------------------------------------------------------
    def do_prompt(self, prompt):
        '''更改命令提示符命令'''
        self.prompt = prompt
    
    #-------------------------------------------------------------------------------
    def do_proconf(self, param):
        '''项目配置'''
        def print_status():
            print "project config status:",self.__project_config
        
        if param == "status":
            return print_status()
        if param == "on":
            self.__project_config = True
            return print_status()
        if param == "off":
            self.__project_config = False
            return print_status()
            
        print "error command param."
    
    #-------------------------------------------------------------------------------
    def complete_proconf(self, text, line, begidx, endidx):
        '''proconf命令自动补全'''
        if not text:
            completions = self.__PROCONF_SUBCOMMAND[:]
        else:
            completions = [subcommand for subcommand in self.__PROCONF_SUBCOMMAND if subcommand.startswith(text)]
            
        return completions
    
    #-------------------------------------------------------------------------------
    def do_show(self, params):
        '''显示项目/RequestEntry命令'''
        params = params.split()
        func = getattr(self, "show_" + params[0])
        func(params[1:])
    
    #-------------------------------------------------------------------------------
    def complete_show(self, text, line, begidx, endidx):
        '''show 命令自动补全'''
        if not text:
            completions = self.__SHOW_SUBCOMMAND[:]
        else:
            completions = [subcommand for subcommand in self.__SHOW_SUBCOMMAND if subcommand.startswith(text)]
            
        return completions
    
    #-------------------------------------------------------------------------------
    def show_projects(self, params):
        '''显示所有项目'''
        if self.__requestProjects is None: return
        for index, requestProject in enumerate(self.__requestProjects):
            print "| Index:", index + 1, "| Name: ", requestProject.getProjectName(), "| Alias:", requestProject.getProjectAlias(), "|"
    
    #-------------------------------------------------------------------------------
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
    
    #-------------------------------------------------------------------------------
    def show_requests(self, params):
        '''显示当前项目下所有request'''
        if self.__currentRequestProject is None:
            print "no project selected."
            return
        first_request_index = 0
        requests_limit = 10
        try:
            if params:
                params_length = len(params)
                if params_length == 1:
                    requests_limit = int(params[0])
                if params_length == 2:
                    first_request_index = int(params[0]) - 1
                    requests_limit = int(params[1])
        except ValueError:
            print "limit param error."
            return
        requestEntrys = self.__getRequestEntrys()[first_request_index:first_request_index + requests_limit]
        for index, requestEntry in enumerate(requestEntrys):
            print index + 1, "--->", requestEntry.getName()
    
    #-------------------------------------------------------------------------------
    def do_exit(self, param):
        '''退出程序命令'''
        return True
    
    #-------------------------------------------------------------------------------
    def do_quit(self, param):
        '''退出程序命令'''
        return True
    
    #-------------------------------------------------------------------------------
    def do_EOF(self, params):
        '''退出程序命令'''
        return True
    
    #-------------------------------------------------------------------------------
    def do_req(self, params):
        '''以RequestEntry请求命令'''
        use_project_config = self.__project_config
        
        if len(params) == 0:
            print "miss param."
            return
            
        try:
            if self.__currentRequestProject is None:
                print "no project selected."
                return
                
            params = params.split()
            if len(params) == 1:
                reqIndex = int(params[0]) - 1
            if len(params) == 2:
                if params[0] == "-u":
                    use_project_config = True
                elif params[0] == "-U":
                    use_project_config = False
                else:
                    print "error command error."
                reqIndex = int(params[1]) - 1
                
            requestEntrys = self.__getRequestEntrys()
            if use_project_config:
                url = self.__currentRequestProject.getProjectHost() + ":" + self.__currentRequestProject.getProjectPort() + "/" + requestEntrys[reqIndex].getUrl()
            else:
                url = requestEntrys[reqIndex].getUrl()
            
            request_params = urllib.urlencode({'data':json.dumps(requestEntrys[reqIndex].getParams())})
            req = urllib2.Request(url, request_params)
            
            try:
                response = urllib2.urlopen(req)
                result = unicode(response.read(),'utf-8')
                print result
            except ValueError:
                print "cannot access url or url error."
        except IndexError:
            print "req index error."
        except ValueError:
            print "limit param error."
        except urllib2.URLError:
            print "cannot access url or url error."
