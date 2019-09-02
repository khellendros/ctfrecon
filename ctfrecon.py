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

class nmapParsedHost:
    hostAddress = ''
    hostMAC = ''
    hostVendor = ''
    osFingerprint = ''
    osCPEproduct = []
    osCPEversion = []
    serviceCPEproduct = []
    serviceCPEversion = []
    serviceName = []
    serviceFingerprint = []
    servicePort = []
    serviceState = []

def open_CSV(PATH):   #open, read all lines from CSV index
    if os.path.isfile(PATH + 'files_exploits.csv') == True:
        exploitCSV = open(PATH + 'files_exploits.csv')
        lines = exploitCSV.readlines()
        exploitCSV.close()    
        return lines
    else:
        print(PATH + 'files_exploits.csv does not exist!')
        sys.exit()
    

def search_exploits(searchStr, csvIndex):   #traverse CSV index and search all files referenced for squery
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

def search_exploits_index(searchStr, csvIndex):
    indexResults = []

    print("\nSearching the index---------------------->SEARCH QUERY: " + searchStr)

    for line in csvIndex[1:]:
        lineLower = line.lower()
        search = lineLower.find(searchStr)

        if search != -1:               
            tmp = line.split(',')    #turning into multidimensional array so displayResults can read it correctly
            indexResults.append(tmp)

    return indexResults

def parse_nmap():
        parsedHosts = []
        parsedHosts = nmapParsedHost
        x = 0
        y = 0
    #if os.path.isfile(xmlNmapPath):
        nmap_data = NmapParser.parse_fromfile('/home/khellendros/SCANS/192.168.1.1/192.168.1.1-tcp.xml')
        for host in nmap_data.hosts:
            parsedHosts[x].hostAddress = host.address                          #Host IP address
            parsedHosts[x].hostVendor = host.vendor                            #Host Vendor
            parsedHosts[x].hostMAC = host.mac                                  #Host MAC Address

            if(host.os_fingerprinted):
                parsedHosts[x].osFingerprint = host.os_fingerprint             #OS Fingerprint

            osMatches = host.os_class_probabilities()
            #OS Matches CPE Parse
            for osMatch in osMatches:
                if osMatch.cpelist:
                    for osCpe in osMatch.cpelist:
                        parsedHosts[x].osCPEproduct[y] = osCpe.get_product()      #OS CPE Product
                        parsedHosts[x].osCPEversion[y] = osCpe.get_version()      #OS CPE Version
                        y += 1
            y = 0
            #Service Parse
            if host.services:
                for s in host.services:
                    if s.cpelist:
                        for c in s.cpelist:
                            parsedHosts[x].serviceCPEproduct[y] = c.get_product() #Service CPE Product
                            parsedHosts[x].serviceCPEversion[y] = c.get_version() #Service CPE Version
                    parsedHosts[x].serviceName[y] = s.service                     #Service name
                    parsedHosts[x].serviceFingerprint[y] = s.servicefp            #Service fingerprint
                    parsedHosts[x].servicePort[y] = s.port                        #Service port
                    parsedHosts[x].serviceState[y] = s.state                      #Service state(open/close)
                    y += 1
            x += 1

def display_results(rList):
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
            
def check_len(someString):
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
        #parse_nmap()
        exit(0)

    for currentArg, currentValue in args:
        if currentArg in ("-d", "--deep"):  #deep also runs index search
            check_len(currentValue)
            results = search_exploits(currentValue.lower(), open_CSV(SSPATH))
            indexResults = search_exploits_index(currentValue.lower(), open_CSV(SSPATH))
            #remove duplicate results
            for x in range(len(results)-1):
                for y in range(len(indexResults)-1):
                    if results[x] == indexResults[y]:
                        print("Deleting: " + indexResults[y][FILE])
                        del indexResults[y]
            for x in range(len(indexResults)-1):
                results.append(indexResults[x])

        elif currentArg in ("-i", "--index"):
            check_len(currentValue)
            results = search_exploits_index(currentValue.lower(), open_CSV(SSPATH))

        if len(results) > 0:
            displayResults(results)
        else:
            print("No results found for: " + currentValue)


	


