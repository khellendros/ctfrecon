from interface.commandhandler import exec_cmd

status = True
while status:
    command = input("ctfRecon> ")
    status = exec_cmd(command)
