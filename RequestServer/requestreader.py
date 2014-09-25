#-*- coding:utf-8 -*-
from requestentry import RequestEntry
from requestproject import RequestProject
from xml.etree import ElementTree

class RequestReader:
    #----------------------------------------------------------------------
    def __init__(self, xmlfile):
	"""init"""
        self.__xmlfile = xmlfile
	self.__root = ElementTree.fromstring(open(self.__xmlfile).read())
    
    #----------------------------------------------------------------------
    def __getRootElement(self):
	"""获取项目根节点"""
	return self.__root
        
    #----------------------------------------------------------------------
    def getRequestProjects(self):
	"""获取所有请求项目"""
        projectsElement = self.__root.find("projects")
        projectItems = projectsElement.getiterator("project")
        projects = []
        for project in projectItems:
            requestEntrys = self.__getRequestUrlEntrys(project)
            projectName = self.__getElementAttributeValue(project, "name")
            projectAlias = self.__getElementAttributeValue(project, "alias")
            projectHost = self.__getElementAttributeValue(project, "host")
            projectPort = self.__getElementAttributeValue(project, "port")
            requestProject = RequestProject(projectName, projectAlias, projectHost, projectPort, requestEntrys)
            projects.append(requestProject)
        return projects
    
    #----------------------------------------------------------------------
    def __getElementAttributeValue(self, srcElement, attrName):
	"""获取给定节点的属性值"""
        if srcElement.get(attrName) is None:
            element = srcElement.find(attrName)
            return element.text
        else:
            return srcElement.get(attrName)
    
    #----------------------------------------------------------------------
    def getRequestEntrys(self, projectElement):
	"""获取给定节点下多有requesturl节点"""
        return projectElement.getiterator("requesturls/requesturl")
    
    #----------------------------------------------------------------------
    def __getChildrenElements(self, rootElement, elementName = "requesturl"):
	"""获取给定节点下的所有子节点"""
        return rootElement.getiterator(elementName)
    
    #----------------------------------------------------------------------
    def __getElement(self, rootElement, elementName):
	"""从根节点获取节点"""
        return rootElement.find(elementName)
    
    #----------------------------------------------------------------------
    def __getRequestUrlEntrys(self, paramElement):
	"""获取指定节点下所有RequestUrlEntry"""
        requesturls = self.__getChildrenElements(paramElement)
        requestEntrys = []
		
        for requesturl in requesturls:
            requestEntry = RequestEntry()
            if requesturl.get("name") is None:
                element = requesturl.find("name")
                requestEntry.setName(element.text)
            else:
                requestEntry.setName(requesturl.get("name"))
            if requesturl.get("url") is None:
                element = requesturl.find("url")
                requestEntry.setUrl(element.text)
            else:
                requestEntry.setUrl(requesturl.get("url"))
            paramsElement = requesturl.find("params")
            params = {}
            
            if paramsElement is None:
                requestEntrys.append(requestEntry)
                continue
            
            for paramElement in paramsElement.getchildren():
                if paramElement.get("paramname") is None:
                    element = paramElement.find("paramname")
                    paramname = element.text
                else:
                    paramname = paramElement.get("paramname")
                   
                if paramElement.get("paramdata") is None:
                    element = paramElement.find("paramdata")
                    paramdata = element.text
                else:
                    paramdata = paramElement.get("paramdata")
                params[paramname] = paramdata
            requestEntry.setParams(params)
            requestEntrys.append(requestEntry)
			
        return requestEntrys