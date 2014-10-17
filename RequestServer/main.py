# _*_ coding:utf-8 _*_
"""程序入口模块"""
import sys
from requestcommand import RequestCommand

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "no projects xml file."
        exit(1)
    PRO_CONF = sys.argv[1]
    REQ_CMD = RequestCommand(PRO_CONF)
    REQ_CMD.cmdloop()
