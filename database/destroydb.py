#!/usr/bin/env python3
from objectmaps import Tool, WordList, ToolChain
from mongoengine import connect, disconnect

connect('ctfrecon_db')

for tools in Tool.objects:
    tools.delete()

for wordlist in WordList.objects:
    wordlist.delete()

for toolchains in ToolChain.objects:
    toolchains.delete()

disconnect()
