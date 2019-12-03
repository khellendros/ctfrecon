from interface.commandhandler import exec_command 


class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = 'global'
        self.prompt = 'ctfrecon# '

    def change_namespace(self, namespace):
        self.namespace = namespace
        self.prompt = namespace + '# '

    def get_cmd(self):
        self.command = input('%s ' % self.prompt)
    
    def exec_cmd(self):
        cmdstatus = exec_command(self)
        return cmdstatus 


interface = CommandLineInterface()
status = True

while status:

    interface.get_cmd()
    status = interface.exec_cmd()

print("Goodbye!")
