import database.dbhandler as dbhandler

class CmdHandler():

    def __init__(self):
        self.cmdlist = []

    def execute(self, cmd):
        if cmd[0] == 'show':
            print('show function')
            return False

