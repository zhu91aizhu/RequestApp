import urllib
import urllib2
import json
from requestreader import RequestReader
from cmd import Cmd

class RequestCommand(Cmd):
    def __init__(self, xmlfile):
        Cmd.__init__(self)
        self.__reqUrlReader = RequestReader(r"requesturl.xml")
        self.__requestProjects = self.__getRequestProjects()
        self.__currentRequestProject = None
        self.prompt = ">>> "
        
    def __getRequestEntrys(self, requestProject):
        return self.__reqUrlReader.getRequestUrlEntrys(requestProject)
        
    def __getRequestProjects(self):
        return self.__reqUrlReader.getRequestProjects()
    
    def do_prompt(self, prompt):
        self.prompt = prompt
    
    def do_show(self, params):
        params = params.split()
        func = getattr(self, "show_" + params[0])
        func(params[1:])
    
    def show_projects(self, params):
        if self.__requestProjects is None: return
        for index, requestProject in enumerate(self.__requestProjects):
            print index + 1, "--->", requestProject.getName()
            
    def do_use(self, projectIndex):
        try:
            projectIndex = int(projectIndex) - 1
        except ValueError:
            print "project param error."
            
        if projectIndex > len(self.__requestProjects) or projectIndex < 0:
            print "project index out arange."
        
        self.__currentRequestProject = self.__requestProjects[projectIndex]
        print "use project ok"
    
    def show_requests(self, limit):
        if self.__currentRequestProject is None:
            print "no project selected."
        
        try:
            param = int(limit[0])
        except ValueError:
            print 'limit param error.'
            return
        requestEntrys = self.__getRequestEntrys(self.__currentRequestProject)
        for index, requestEntry in enumerate(requestEntrys):
            if index >= param: break
            print index + 1, "--->", requestEntry.getName()
    
    def do_exit(self, param):
        return True
        
    def do_quit(self, param):
        return True
    
    def do_req(self, requestIndex):
        try:
            reqIndex = int(requestIndex) - 1
        except ValueError:
            print 'limit param error.'
            return
            
        requestEntrys = self.__getRequestEntrys(self.__currentRequestProject)
        url = requestEntrys[reqIndex].getUrl()
        params = urllib.urlencode({'data':json.dumps(requestEntrys[reqIndex].getParams())})
        req = urllib2.Request(url, params)
        response = urllib2.urlopen(req)
        result = unicode(response.read(),'utf-8')
        
        print result