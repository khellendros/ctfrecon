import interface.commandhandler as cmdhandler

class NameSpace():
    def __init__(self):
        self.project = ''
        self.domain = ''
        self.level = 1

    def change(self, project='', domain='', level=0):
        self.project = project 
        self.domain = domain 
        self.level = level 
        return 'OK'

class CommandLineInterface():

    def __init__(self):
        self.command = ''
        self.namespace = NameSpace()
        self.commandlist = {'show': cmdhandler.show_cmd, 
                            'use': cmdhandler.use_cmd,
                            'add': cmdhandler.add_cmd, 
                            'set': cmdhandler.set_cmd, 
                            'run': cmdhandler.run_cmd, 
                            'exit': cmdhandler.exit_ctfrecon, 
                            'quit': cmdhandler.exit_ctfrecon,
                            'help': self.display_help} 

    def setprompt(self):
        self.prompt = '%s::%s#' % (self.namespace.project, self.namespace.domain)

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
        if self.namespace.level > 0:
            print('show projects\n'
                'use project [project]\n'
                'add project [project]\n'
                'show tools\n'
                'add tool\n'
                'show toolchains\n'
                'add toolchain\n'
                )
        if self.namespace.level == 2:
            print('show domains\n'
                'use domain [domain]\n'
                )
        return 'OK' 
