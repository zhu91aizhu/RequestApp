class RequestProject:
    def __init__(self, name = "", alias = "", host = "127.0.0.1", port = "8080", requestEntrys = None):
        self.__name = name
        self.__alias = alias
        self.__host = host
        self.__port = port
        self.__requestEntrys = requestEntrys
        
    def getRequestEntrys(self):
        return self.__requestEntrys
        
    def getProjectHost(self):
        return self.__host
        
    def getProjectPort(self):
        return self.__port
        
    def getProjectName(self):
        return self.__name
    
    def getProjectAlias(self):
        return self.__alias