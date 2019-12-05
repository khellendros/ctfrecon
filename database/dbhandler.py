from mongoengine import connect, disconnect
from database.objectmaps import *

def mongo_connect():
    connect('ctfrecon_db')

def mongo_disconnect():
    disconnect('ctfrecon_db')

def show_db(cli):
    enumlist = []
    mongo_connect()

    if (cli.cmd_breakout[1] == 'projects'):
        for enum in Enumeration.objects:
            enumlist.append(enum.project)
    elif (cli.cmd_breakout[1] == 'domains'):
        for enum in Enumeration.objects(project=cli.namespace.project):
            enumlist.append(enum.domain)
    elif (cli.cmd_breakout[1] == 'tools'):
        for tool in Tool.objects:  
            enumlist.append(tool.alias)
    elif (cli.cmd_breakout[1] == 'toolchains'):
        for toolchain in ToolChain.objects:
            enumlist.append(toolchain.name)

    if enumlist is not None:
        cli.display_list(enumlist)

    mongo_disconnect()  
    return 'OK'

def validate_namespace(cli):
    mongo_connect()
    status = False

    if (cli.cmd_breakout[1] == 'project'):
        for enum in Enumeration.objects:
            if (enum.project == cli.cmd_breakout[2]):
                status = True
    elif (cli.cmd_breakout[1] == 'domain'):
        for enum in Enumeration.objects:
            if (enum.domain == cli.cmd_breakout[2]):
                status = True
    
    mongo_disconnect()
    return status
