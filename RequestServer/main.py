# _*_ coding:utf-8 _*_
"""程序入口模块"""
from requestcommand import RequestCommand

if __name__ == "__main__":
    REQ_CMD = RequestCommand(r"requesturl.xml")
    REQ_CMD.cmdloop()
