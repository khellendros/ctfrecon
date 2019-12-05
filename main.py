#!/usr/bin/env python3

from interface.interactive import CommandLineInterface

if __name__ == '__main__':
    interface = CommandLineInterface()
    status = True                     

    while True:
        interface.setprompt()
        interface.get_cmd()
        status = interface.exec_cmd()    
        if (status != 'OK'):             
            interface.display_msg(status)


