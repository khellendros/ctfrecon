import interface.commandhandler as cmdhandler


class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = 'global'
        self.prompt = 'ctfrecon# '
        self.commandlist = {'show': cmdhandler.show_cmd, 
                            'use': cmdhandler.use_cmd,
                            'add': cmdhandler.add_cmd, 
                            'set': cmdhandler.set_cmd, 
                            'run': cmdhandler.run_cmd, 
                            'exit': cmdhandler.exit_ctfrecon, 
                            'quit': cmdhandler.exit_ctfrecon,
                            'help': self.display_help} 

    def change_namespace(self, namespace):
        self.namespace = namespace
        self.prompt = namespace + '# '

    def get_cmd(self):
        self.command = ''
        self.cmd_breakout = []
        self.command = input('%s ' % self.prompt)
        self.command = self.command.lower()
        self.cmd_breakout = self.command.split(' ')
    
    def exec_cmd(self):
        cmdstatus = self.commandlist.get(self.cmd_breakout[0], cmdhandler.no_cmd)(self)
        return cmdstatus

    def display_msg(self, message):
        print('--- {} ---'.format(message))

    def display_help(self, throwaway):
        if self.namespace is 'global':
            print('\nGlobal Namespace Commands:\n'
                  '--------------------------\n'
                  'show projects\n'
                  'use project [project]\n'
                  'add project [project]\n'
                  'show tools\n'
                  'add tool\n'
                  'show toolchains\n'
                  'add toolchain\n'
                 )
        return True
                    

interface = CommandLineInterface()
status = True

while status:
    interface.get_cmd()
    status = interface.exec_cmd()
