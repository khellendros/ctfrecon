import sys
import os
import database.dbhandler as dbhandler

def use_cmd(cli):
    if (len(cli.cmd_breakout) < 3):
        subcmd = None
        namespace = None
        status = 'Invalid number of arguments to "use", try using "help"'
    else:
        subcmd = cli.cmd_breakout[1]
        namespace = cli.cmd_breakout[2]
        status = 'Invalid argument to "use", try using "help"'


    if (subcmd == 'project'):
        if (dbhandler.validate_namespace(cli)):
            status = cli.change_namespace(namespace, 2)
        else:
            status = '{} does not exist!'.format(subcmd)
    elif (subcmd == 'domain') and (cli.namespace_lvl >= 2):
        if (dbhandler.validate_namespace(cli)):
            status = cli.change_namespace(namespace, 3)
        else:
           status = '{} does not exist!'.format(subcmd)
    
    return status 


def show_cmd(cli):
    if (len(cli.cmd_breakout) < 2):
        subcmd = None
        status = 'Invalid number of arguments to "show", try using "help"'
    else:
        subcmd = cli.cmd_breakout[1]
        status = 'Invalid argument to "show", try using "help"'


    if (subcmd == 'projects'):
        status = dbhandler.show_db(cli)
    elif (subcmd == 'tools'):
        status = dbhandler.show_db(cli)
    elif (subcmd == 'toolchains'):
        status = dbhandler.show_db(cli)
    
    if (cli.namespace_lvl > 1):
        if (subcmd == 'domains'):
            status = dbhandler.show_db(cli)

    if (cli.namespace_lvl > 2):
        # validate and display enumeration attribute here
        if (subcmd == 'enum'):
            status = cli.display_msg('show enum')

    return status 


def add_cmd(cli):
    return True;


def set_cmd(cli):
    return True;


def run_cmd(cli):
    return True;


def exit_ctfrecon(cli):
    exit(0)

def no_cmd(cli):
    if cli.cmd_breakout[0] == 'cd' and len(cli.cmd_breakout) > 1:
        try:
            os.chdir(cli.cmd_breakout[1])
        except: 
            e = sys.exc_info()[0]
            print(e)
    else:
        os.system(cli.command)
    return 'OK' 



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
    
