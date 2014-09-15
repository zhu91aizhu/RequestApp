#-*- coding:utf-8 -*-
from requestentry import RequestEntry
from xml.etree import ElementTree

class RequestReader:
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.root = ElementTree.fromstring(open(self.xmlfile).read())
	
	def __getRootElement(self, xmlfile = self.xmlfile):
		root = ElementTree.fromstring(open(xmlfile).read())
		return root
        
    def getRequestProjects(self):
        return self.__root.getiterator("projects")
        
    def getRequestUrls(self, projectElement):
        return projectElement.getiterator("requesturls/requesturl")
		
    def __getChildrenElements(self, rootElement, elementName = "requesturl"):
        return rootElement.getiterator(elementName)
		
    def __getElement(self, rootElement, elementName):
        return rootElement.find(elementName)
		
    def getRequestUrlEntrys(self):
        requesturls = self.__getChildrenElements(self.root)
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