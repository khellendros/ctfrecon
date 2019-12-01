#! /usr/bin/env python3
from objectmaps import *

connect('ctfrecon_default')

for tools in Tool.objects:
    tools.delete()

for wordlist in WordList.objects:
    wordlist.delete()

for toolchains in ToolChain.objects:
    toolchains.delete()

disconnect()
