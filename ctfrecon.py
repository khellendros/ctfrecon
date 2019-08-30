#! /usr/bin/python3

import sys, os, getopt, pydoc 

#-------------CSV Identifiers------------
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
unixOptions = "d:s:h"
gnuOptions = ["deep=", "surface=", "help"]



def openCSV(PATH):   #open, read all lines from CSV index
    if os.path.isfile(PATH + 'files_exploits.csv') == True:
        exploitCSV = open(PATH + 'files_exploits.csv')
        lines = exploitCSV.readlines()
        exploitCSV.close()    
        return lines
    else:
        print(PATH + 'files_exploits.csv does not exist!')
        sys.exit()
    

def deepsearch(searchStr, csvIndex):   #traverse CSV index and search all files referenced for squery
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
                    for contentLine in exploitFileContent:              #SEearch through file one line at a time - TODO: also search CSV index 
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


def displayResults(rList):
    select = 1
    x = 1 

    while select != 0:
        for r in rList:
            print(f"\n\033[1;32;40m{x})\033[1;31;40mFILE: \033[1;32;40m {r[FILE]} \033[1;31;40m")
            print(f"  DESCRIPTION: \033[1;32;40m {r[DESCRIPTION]} \033[1;31;40m")
            print(f"  DATE: \033[1;32;40m {r[DATE]} \033[1;31;40m")
            print(f"  AUTHOR: \033[1;32;40m {r[AUTHOR]} \033[1;31;40m")
            print(f"  TYPE: \033[1;32;40m {r[TYPE]} \033[1;31;40m")
            print(f"  PLATFORM: \033[1;32;40m {r[PLATFORM]} \033[1;31;40m")
            print(f"  PORT: \033[1;32;40m {r[PORT]} \n")
            x = x + 1

        print("(0 to Exit)------------------->", end=' ')
        select = int(input())

        if select == 0:
            return 0
        elif select < x and select > -1:
            if (os.path.isfile(SSPATH + rList[select - 1][FILE])) == True:
                with open(SSPATH + rList[select - 1][FILE], 'r') as exploitFILE:
                    textFile = exploitFILE.read()
                    pydoc.pager(textFile)
                    exploitFILE.close()
        else:
            print("\nNo such index!\n")

        x = 1
            


if __name__ == "__main__":

    commandArgs = sys.argv[1:]

    try:
        args, argvalue = getopt.getopt(commandArgs, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " -d SEARCHQUERY")
        exit(0)

    for currentArg, currentValue in args:
        if currentArg in ("-d", "--deep"):  #TODO:errorcheck currentValue to make sure search string is not too short resulting in too much output
            results = deepsearch(currentValue.lower(), openCSV(SSPATH))
            if results is not None:  #this is hilarious
                displayResults(results)
            else:
                print("No results found for: " + currentValue)
            
