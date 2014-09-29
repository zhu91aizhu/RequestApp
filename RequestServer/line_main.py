from requestcommand import RequestCommand

def main(xml_file):
    reqCmd = RequestCommand(xml_file)
    reqCmd.cmdloop()
