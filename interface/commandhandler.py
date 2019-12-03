import database.dbhandler as dbhandler

def change_namespace(cli):

    newnamespace = 'project'
    cli.change_namespace(newnamespace)
    print('change namespace')
    return True;


def show_cmd(cli):

    print('show command')
    return True


def add_cmd(cli):

    return True;


def set_cmd(cli):

    return True;


def run_cmd(cli):

    return True;


def exit_ctfrecon(cli):

    return False;


def no_cmd(cli):

    return 'Unkown Command'



commandlist = { 'show': show_cmd, 'use': change_namespace, 'add': add_cmd, 
                'set': set_cmd, 'run': run_cmd, 'exit': exit_ctfrecon, 
                'quit': exit_ctfrecon}

def exec_command(cli):
   
    cmd_breakout = cli.command.split(' ')
    status = commandlist.get(cmd_breakout[0], no_cmd)(cli)

    return status 


""" 

    GLOBAL NAMESPACE:
    -----------------
    show TOOLS
    show TOOLCHAINS
    add TOOL
    add TOOLCHAIN

    show PROJECTS
    use PROJECT
    add PROJECT

    PROJECT NAMESPACE:
    ------------------
    show DOMAINS
    use DOMAIN
    add DOMAIN

    DOMAIN NAMESPACE:
    -----------------------
    set IPADDRESS
    set NOTE
    set FOI

    show enum ALL
    show enum TOOL
    show enum NOTE
    show enum FOI

    run TOOLCHAIN NAME 
    run TOOL ALIAS
"""
    
