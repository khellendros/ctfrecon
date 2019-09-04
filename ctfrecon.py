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
unixOptions = "d:i:x:"
gnuOptions = ["deep=", "index=", "nmapXML="]

class nmapParsedHost:
    def __init__(self, hostAddress=None, hostMAC=None, hostVendor=None, osFingerprint=None):
        self.hostAddress = hostAddress 
        self.hostMAC = hostMAC 
        self.hostVendor = hostVendor 
        self.osFingerprint = osFingerprint 
        self.osCPEproduct = [] 
        self.osCPEversion = [] 
        self.serviceCPEproduct = [] 
        self.serviceCPEversion = []
        self.serviceName = []
        self.serviceFingerprint = []
        self.servicePort = []
        self.serviceState = []
    def addOScpeProduct(self, cpeProduct):
        self.osCPEproduct.append(cpeProduct)
    def addOScpeVersion(self, cpeVersion):
        self.osCPEversion.append(cpeVersion)
    def addServiceName(self, sName):
        self.serviceName.append(sName)
    def addServiceFingerprint(self, sFingerprint):
        self.serviceFingerprint.append(sFingerprint)
    def addServicePort(self, sPort):
        self.servicePort.append(sPort)
    def addServiceState(self, sState):
        self.serviceState.append(sState)
    def addServiceCPEproduct(self, cpeProduct):
        self.serviceCPEproduct.append(cpeProduct)
    def addServiceCPEversion(self, cpeVersion):
        self.serviceCPEversion.append(cpeVersion)

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

def parse_nmap(xmlNmapPath):
    parsedHosts = [] 
    x = 0
    if os.path.isfile(xmlNmapPath):
        nmap_data = NmapParser.parse_fromfile(xmlNmapPath)
        for host in nmap_data.hosts:
            parsedHosts.append(nmapParsedHost(host.address, host.vendor, host.mac)) 

            if(host.os_fingerprinted):
                parsedHosts[x].osFingerprint = host.os_fingerprint              #OS Fingerprint

            osMatches = host.os_class_probabilities()
            #OS Matches CPE Parse
            for osMatch in osMatches:
                if osMatch.cpelist:
                    for osCpe in osMatch.cpelist:
                        parsedHosts[x].addOScpeProduct(osCpe.get_product())     #OS CPE Product
                        parsedHosts[x].addOScpeVersion(osCpe.get_version())     #OS CPE Version
            #Services Parse
            if host.services:
                for s in host.services:
                    if s.cpelist:
                        for c in s.cpelist:
                            parsedHosts[x].addServiceCPEproduct(c.get_product())#Service CPE Product
                            parsedHosts[x].addServiceCPEversion(c.get_version())#Service CPE Version
                    parsedHosts[x].addServiceName(s.service)                    #Service name
                    parsedHosts[x].addServiceFingerprint(s.servicefp)           #Service fingerprint
                    parsedHosts[x].addServicePort(s.port)                       #Service port
                    parsedHosts[x].addServiceState(s.state)                     #Service state(open/close)
            x += 1
    return parsedHosts[0].serviceCPEproduct[0] + " " + parsedHosts[0].serviceCPEversion[0]

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

def remove_duplicates(results1, results2):
    #remove duplicate results
    for x in range(len(results1)-1):
        for y in range(len(results2)-1):
            if results1[x] == results2[y]:
                del indexResults[y]
        for x in range(len(indexResults)-1):
            results1.append(results2[x])
    return results1


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
        print("   Nmap XML Search:" + sys.argv[0] + " -x XML_FILE")
        exit(0)

    for currentArg, currentValue in args:
        if currentArg in ("-x", "--nmapXML"):
            results = search_exploits(parse_nmap(currentValue), open_CSV(SSPATH))
            indexResults = search_exploits_index(parse_nmap(currentValue), open_CSV(SSPATH))
            remove_duplicates(results, indexResults)
            break
        elif currentArg in ("-d", "--deep"):  #deep also runs index search
            check_len(currentValue)
            results = search_exploits(currentValue.lower(), open_CSV(SSPATH))
            indexResults = search_exploits_index(currentValue.lower(), open_CSV(SSPATH))
            remove_duplicates(results, indexResults)
            break
        elif currentArg in ("-i", "--index"):
            check_len(currentValue)
            results = search_exploits_index(currentValue.lower(), open_CSV(SSPATH))
            break

    if len(results) > 0:
        display_results(results)
    else:
        print("No results found for: " + currentValue)
