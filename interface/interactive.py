from interface.commandhandler import exec_cmd

class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = 'global'
        self.prompt = 'ctfrecon# '

    def get_cmd(self):

        self.cmdbreakout = []
        self.command = input('%s ' % self.prompt)
        self.cmdbreakout = self.command.split(' ')
    
    def exec_cmd(self)
        
        return False


interface = CommandLineInterface()
status = True

while status:
    interface.get_cmd()
    status = interface.exec_cmd(command.cmdbreakout)
