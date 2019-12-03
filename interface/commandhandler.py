import database.dbhandler as dbhandler

def use_cmd(cli):
    newnamespace = 'project'
    cli.change_namespace(newnamespace)
    print('change namespace')
    return True;


def show_cmd(cli):
    if len(cli.cmd_breakout) < 2:
        cli.display_msg('Invalid number of arguments to "show" --try "help"')
        return True

    if cli.cmd_breakout[1] == 'projects':
        cli.display_msg('show projects')
        return True
    elif cli.cmd_breakout[1] == 'tools':
        cli.display_msg('show tools')
        return True
    elif cli.cmd_breakout[1] == 'toolchains':
        cli.display_msg('show toolchains')
        return True
    
    if cli.namespace == 'project':
        
        if cli.cmd_breakout[1] == 'domains':
            cli.display_msg('show domains')
            return True
        else:
            cli.display_msg('Unknown option for show in %s namespace' % cli.namespace)
            return True

    elif cli.namespace == 'domain':

        # validate and display enumeration attribute here
        if cli.cmd_breakout[1] == 'enum':
            cli.display_msg('show enum')
            return True


    return True


def add_cmd(cli):
    return True;


def set_cmd(cli):
    return True;


def run_cmd(cli):
    return True;


def exit_ctfrecon(cli):
    cli.display_msg('Goodbye!')
    return False;


def no_cmd(cli):
    cli.display_msg('Unknown Command!')
    return True 



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
    
