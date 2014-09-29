# _*_ coding:utf-8 _*_
"""请求项目模块"""

class RequestProject(object):
    """请求项目类"""

    def __init__(self, name="", requestEntrys=None):
        """init"""
        self.__name = name
        self.__alias = ""
        self.__host = ""
        self.__port = ""
        self.__request_entrys = requestEntrys

    def get_request_entrys(self):
        """获取所有请求实体"""
        return self.__request_entrys

    def get_project_host(self):
        """获取项目主机名称"""
        return self.__host

    def set_project_host(self, host):
        """设置项目主机名称"""
        self.__host = host

    def get_project_port(self):
        """获取项目端口号"""
        return self.__port

    def set_project_port(self, port):
        """设置项目端口号"""
        self.__port = port

    def get_project_name(self):
        """获取项目名称"""
        return self.__name

    def get_project_alias(self):
        """获取项目别名"""
        return self.__alias

    def set_project_alias(self, alias):
        """设置项目别名"""
        self.__alias = alias
