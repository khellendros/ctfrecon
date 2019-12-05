import interface.commandhandler as cmdhandler


class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = 'ctfrecon'
        self.namespace_lvl = 1 
        self.prompt = 'ctfrecon# '
        self.commandlist = {'show': cmdhandler.show_cmd, 
                            'use': cmdhandler.use_cmd,
                            'add': cmdhandler.add_cmd, 
                            'set': cmdhandler.set_cmd, 
                            'run': cmdhandler.run_cmd, 
                            'exit': cmdhandler.exit_ctfrecon, 
                            'quit': cmdhandler.exit_ctfrecon,
                            'help': self.display_help} 

    def change_namespace(self, namespace, namespace_lvl):
        self.namespace = namespace
        self.namespace_lvl = namespace_lvl
        self.prompt = namespace + '# '

    def get_cmd(self):
        self.command = ''
        self.cmd_breakout = []
        self.command = input('%s ' % self.prompt)
        self.cmd_breakout = self.command.split(' ')
        if (len(self.cmd_breakout) > 0):
            self.cmd_breakout[0] = self.cmd_breakout[0].lower()
    
    def exec_cmd(self):
        cmdstatus = self.commandlist.get(self.cmd_breakout[0], cmdhandler.no_cmd)(self)
        return cmdstatus

    def display_msg(self, message):
        print('--- {} ---'.format(message))

    def display_list(self, outputlist):
        print()
        for listitem in outputlist:
            print(" {} ".format(listitem))
        print()

    def display_help(self, throwaway):
        print('\nCommands:\n'
              '---------\n')
        if self.namespace_lvl > 0:
            print('show projects\n'
                'use project [project]\n'
                'add project [project]\n'
                'show tools\n'
                'add tool\n'
                'show toolchains\n'
                'add toolchain\n'
                )

        return 'OK' 
                    

interface = CommandLineInterface()
status = True

while True:
    interface.get_cmd()
    status = interface.exec_cmd()
    if (status != 'OK'):
        interface.display_msg(status)
