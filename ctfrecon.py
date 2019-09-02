#! /usr/bin/python3

import sys, os, getopt, pydoc 
from libnmap.parser import NmapParser

#-------------CSV Identifiers--------------
ID = 0
FILE = 1
DESCRIPTION = 2
DATE = 3
AUTHOR = 4
TYPE = 5
PLATFORM = 6
PORT = 7
#-----------------------------------------
SSPATH = '/usr/share/exploitdb/' #searchsploit root dir
#------------------OPTIONS----------------
unixOptions = "d:i:h"
gnuOptions = ["deep=", "index=", "help"]



def openCSV(PATH):   #open, read all lines from CSV index
    if os.path.isfile(PATH + 'files_exploits.csv') == True:
        exploitCSV = open(PATH + 'files_exploits.csv')
        lines = exploitCSV.readlines()
        exploitCSV.close()    
        return lines
    else:
        print(PATH + 'files_exploits.csv does not exist!')
        sys.exit()
    

def searchExploits(searchStr, csvIndex):   #traverse CSV index and search all files referenced for squery
    indexResults = [] 

    print("\nWe're Going Deep!------------------------>SEARCH QUERY: " + searchStr)
    
    for line in csvIndex[1:]:                                           #loop through each line in the index 
        line.strip('/n')           
        tmp = line.split(',')                                           #pull each value into a list
        exploitsFilePath = SSPATH + tmp[FILE]                           #set to current lines file value 
        if os.path.isfile(exploitsFilePath) == True:                    #make sure file exists, skip if it doesn't
            with open(exploitsFilePath, 'r') as exploitFILE:
                try:
                    exploitFileContent = exploitFILE.readlines()
                    for contentLine in exploitFileContent:               
                        contentLine = contentLine.lower()
                        search = contentLine.find(searchStr)

                        if search != -1:
                            indexResults.append(tmp)
                            break       #break to prevent duplicate results
                except:
                    print('Some sort of error occured: ',  sys.exc_info()[0])  #TODO: Do proper error handling here

                    exploitFileContent.clear
                    exploitFILE.close
        else:
            print('Skipping ' + exploitsfilepath + '  Does not exist!')
    
    return indexResults

def searchExploitsIndex(searchStr, csvIndex):
    indexResults = []

    print("\nSearching the index---------------------->SEARCH QUERY: " + searchStr)

    for line in csvIndex[1:]:
        lineLower = line.lower()
        search = lineLower.find(searchStr)

        if search != -1:               
            tmp = line.split(',')    #turning into multidimensional array so displayResults can read it correctly
            indexResults.append(tmp)

    return indexResults

def parseNmap():
    #if os.path.isfile(xmlNmapPath):
        nmap_data = NmapParser.parse_fromfile('/home/khellendros/SCANS/192.168.1.1/192.168.1.1-tcp.xml')
        for host in nmap_data.hosts:
            print("\nHost Address: {0}".format(host.address))
            if(host.os_fingerprinted):
                print("OS Fingerprint: {0}".format(host.os_fingerprint))

            osMatches = host.os_class_probabilities()
            for osMatch in osMatches:
                if osMatch.cpelist:
                    for osCpe in osMatch.cpelist:
                        print("Product: " + osCpe.get_product() + " Version: " + osCpe.get_version())
            print("MAC: {0}".format(host.mac))
            print("Vendor: {0}".format(host.vendor))
            print("--------------------------------")
            if host.services:
                for s in host.services:
                    if s.cpelist:
                        for c in s.cpelist:
                            print("\nProduct: " + c.get_product() + " Version: " + c.get_version())
                    print("Service: {0}".format(s.service))
                    print("Service Fingerprint: {0}".format(s.servicefp))
                    print("Port: {0}".format(s.port))
                    print("State: {0}".format(s.state))
                    print("--------------------------------")

def displayResults(rList):
    select = 1
    x = 1 

    while select != 0:
        for r in rList:
            print(f"\033[1;32;40m{x})\033[1;31;40mFILE: \033[1;32;40m {r[FILE]} \033[1;31;40m")
            print(f"  DESCRIPTION: \033[1;32;40m {r[DESCRIPTION]} \033[1;31;40m")
            print(f"  DATE: \033[1;32;40m {r[DATE]} \033[1;31;40m")
            print(f"  AUTHOR: \033[1;32;40m {r[AUTHOR]} \033[1;31;40m")
            print(f"  TYPE: \033[1;32;40m {r[TYPE]} \033[1;31;40m")
            print(f"  PLATFORM: \033[1;32;40m {r[PLATFORM]} \033[1;31;40m")
            print(f"  PORT: \033[1;32;40m {r[PORT]}")
            x = x + 1

        print("(0 to Exit)------------------->", end=' ')
        select = int(input())

        if select == 0:
            return 0
        elif select < x and select > -1:   #TODO: Need to fix error handling for other keyboard inputs besides integers.. like arrows and shit
            if (os.path.isfile(SSPATH + rList[select - 1][FILE])) == True:
                with open(SSPATH + rList[select - 1][FILE], 'r') as exploitFILE:
                    textFile = exploitFILE.read()
                    pydoc.pager(textFile)
                    exploitFILE.close()
        else:
            print("\nNo such index!\n")

        x = 1
            
def checkLen(someString):
    if len(someString) < 4:
        print("Search string too short!")
        exit(0)

if __name__ == "__main__":

    commandArgs = sys.argv[1:]

    try:
        args, argvalue = getopt.getopt(commandArgs, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    if len(sys.argv) < 2:
        print("Usage: Deep Search:" + sys.argv[0] + " -d SEARCHQUERY")
        print("      Index Search:" + sys.argv[0] + " -i SEARCHQUERY")
        parseNmap()
        exit(0)

    for currentArg, currentValue in args:
        if currentArg in ("-d", "--deep"):  #deep also runs index search
            checkLen(currentValue)
            results = searchExploits(currentValue.lower(), openCSV(SSPATH))
            indexResults = searchExploitsIndex(currentValue.lower(), openCSV(SSPATH))
            #remove duplicate results
            for x in range(len(results)-1):
                for y in range(len(indexResults)-1):
                    if results[x] == indexResults[y]:
                        print("Deleting: " + indexResults[y][FILE])
                        del indexResults[y]
            for x in range(len(indexResults)-1):
                results.append(indexResults[x])

        elif currentArg in ("-i", "--index"):
            checkLen(currentValue)
            results = searchExploitsIndex(currentValue.lower(), openCSV(SSPATH))

        if len(results) > 0:
            displayResults(results)
        else:
            print("No results found for: " + currentValue)


	


