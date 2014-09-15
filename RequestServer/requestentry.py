class RequestEntry:
    
    def __init__(self, url = None, name = None, params = None):
        self.__url = url
        self.__name = name
        self.__params = params
        
    def toString(self):
        return "{name: " + self.name + "\nurl: " + self.url + "}\n"
        
    def setUrl(self, url):
        self.__url = url
    
    def getUrl(self):
        return self.__url
    
    def setName(self, name):
        self.__name = name
        
    def getName(self):
        return self.__name
        
    def setParams(self, params):
        self.__params = params
        
    def getParams(self):
        return self.__params