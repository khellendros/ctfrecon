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
        for enum in Enumeration.objects(project=cli.namespace):
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

