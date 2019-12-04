#!/usr/bin/env python3
# Create default MongoDB Collections
from objectmaps import Tool, WordList, ToolChain, Enumeration
from mongoengine import connect, disconnect

connect('ctfrecon_db')

# Wordlists
default_wordlist = WordList(name='mega web discovery', lists=['/opt/github/SecLists/Discovery/Web-Content/big.txt',
                                                     '/opt/github/SecLists/Discovery/Web-Content/raft-large-files.txt',
                                                     '/opt/github/SecLists/Discovery/Web-Content/raft-large-directories.txt'])
default_wordlist.save()


# Tools
default_tool = Tool(alias='gobuster', command='gobuster dir -w $wordlist -u $prefix$domain')
default_tool.save()
default_tool = Tool(alias='nmap full', command='nmap -T4 -A -p - $ipaddress')
default_tool.save()

# Tool Chains
default_toolchain = ToolChain(name='initial discovery', tools=['gobuster', 'nmap full'])
default_toolchain.save()

# Enumerations
test_enum = Enumeration(project='json', domain='json.htb', ipaddress='10.10.10.145')
test_enum.save()

disconnect()
