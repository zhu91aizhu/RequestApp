#-*- coding:utf-8 -*-
"""xml文件读取模块"""

from requestentry import RequestEntry
from requestproject import RequestProject
from xml.etree import ElementTree

class RequestReader(object):
    """xml文件读取工具类"""
    #----------------------------------------------------------------------
    def __init__(self, xmlfile):
        """init"""
        self.__xmlfile = xmlfile
        self.__root = ElementTree.fromstring(open(self.__xmlfile).read())

    #----------------------------------------------------------------------
    def __get_root_element(self):
        """获取项目根节点"""
        return self.__root

    #----------------------------------------------------------------------
    def get_request_projects(self):
        """获取所有请求项目"""
        projects_element = self.__root.find("projects")
        project_items = projects_element.getiterator("project")
        projects = []
        for project in project_items:
            request_entrys = self.__get_requesturl_entrys(project)
            project_name = self.__get_element_attribute_value(project, "name")
            project_alias = self.__get_element_attribute_value(project, "alias")
            project_host = self.__get_element_attribute_value(project, "host")
            project_port = self.__get_element_attribute_value(project, "port")
            request_project = RequestProject(project_name, request_entrys)
            request_project.set_project_host(project_host)
            request_project.set_project_alias(project_alias)
            request_project.set_project_port(project_port)
            projects.append(request_project)
        return projects

    #----------------------------------------------------------------------
    @classmethod
    def __get_element_attribute_value(cls, src_element, attr_name):
        """获取给定节点的属性值"""
        if src_element.get(attr_name) is None:
            element = src_element.find(attr_name)
            return element.text
        else:
            return src_element.get(attr_name)

    #----------------------------------------------------------------------
    @classmethod
    def get_request_entrys(cls, project_element):
        """获取给定节点下多有requesturl节点"""
        return project_element.getiterator("requesturls/requesturl")

    #----------------------------------------------------------------------
    @classmethod
    def __get_children_elements(cls, root_element, element_name="requesturl"):
        """获取给定节点下的所有子节点"""
        return root_element.getiterator(element_name)

    #----------------------------------------------------------------------
    @classmethod
    def __get_element(cls, root_element, element_name):
        """从根节点获取节点"""
        return root_element.find(element_name)

    #----------------------------------------------------------------------
    def __get_requesturl_entrys(self, param_element):
        """获取指定节点下所有RequestUrlEntry"""
        requesturls = self.__get_children_elements(param_element)
        request_entrys = []

        for requesturl in requesturls:
            request_entry = RequestEntry()
            if requesturl.get("name") is None:
                element = requesturl.find("name")
                request_entry.set_name(element.text)
            else:
                request_entry.set_name(requesturl.get("name"))
            if requesturl.get("url") is None:
                element = requesturl.find("url")
                request_entry.set_url(element.text)
            else:
                request_entry.set_url(requesturl.get("url"))
            params_element = requesturl.find("params")
            params = {}

            if params_element is None:
                request_entrys.append(request_entry)
                continue

            for param_element in params_element.getchildren():
                if param_element.get("paramname") is None:
                    element = param_element.find("paramname")
                    paramname = element.text
                else:
                    paramname = param_element.get("paramname")

                if param_element.get("paramdata") is None:
                    element = param_element.find("paramdata")
                    paramdata = element.text
                else:
                    paramdata = param_element.get("paramdata")
                params[paramname] = paramdata
            request_entry.set_params(params)
            request_entrys.append(request_entry)

        return request_entrys
