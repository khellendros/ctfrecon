#! /usr/bin/env python3
from objectmaps import *

connect(alias='ctfrecon_db_alias', db='ctfrecon_db')

for wordlist in WordList.objects:
    print(wordlist.name)
    print(wordlist.lists)

for tool in Tool.objects:
    print(tool.alias)
    print(tool.command)

for toolchain in ToolChain.objects:
    print(toolchain.name)
    print(toolchain.tools)

disconnect()
