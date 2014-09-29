# _*_ coding:utf-8 _*_
"""请求实体模块"""

class RequestEntry(object):
    """请求实体类"""

    def __init__(self, url=None, name=None, params=None):
        self.__url = url
        self.__name = name
        self.__params = params

    def to_string(self):
        """实例信息转换为字符串"""
        return "{name: " + self.__name + "\nurl: " + self.__url + "}\n"

    def set_url(self, url):
        """设置url"""
        self.__url = url

    def get_url(self):
        """获取url"""
        return self.__url

    def set_name(self, name):
        """设置名称"""
        self.__name = name

    def get_name(self):
        """获取名称"""
        return self.__name

    def set_params(self, params):
        """设置参数列表"""
        self.__params = params

    def get_params(self):
        """获取参数列表"""
        return self.__params
