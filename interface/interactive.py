from interface.commandhandler import CmdHandler 

class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = 'global'
        self.prompt = 'ctfrecon# '
        self.cmdhandler = CmdHandler()

    def get_cmd(self):

        self.cmdbreakout = []
        self.command = input('%s ' % self.prompt)
        self.cmdbreakout = self.command.split(' ')
    
    def exec_cmd(self):
   
        cmdstatus = self.cmdhandler.execute(self.cmdbreakout)
        return cmdstatus 


interface = CommandLineInterface()
status = True

while status:
    interface.get_cmd()
    status = interface.exec_cmd()
