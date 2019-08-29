import sys, os, getopt

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
    x = 0 
    foundFilePaths = []

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
                            print(f"\033[1;32;40m{x+1})\033[1;31;40mFILE: \033[1;32;40m {tmp[FILE]} \033[1;31;40m")
                            print(f"  DESCRIPTION: \033[1;32;40m {tmp[DESCRIPTION]} \033[1;31;40m")
                            print(f"  DATE: \033[1;32;40m {tmp[DATE]} \033[1;31;40m")
                            print(f"  AUTHOR: \033[1;32;40m {tmp[AUTHOR]} \033[1;31;40m")
                            print(f"  TYPE: \033[1;32;40m {tmp[TYPE]} \033[1;31;40m")
                            print(f"  PLATFORM: \033[1;32;40m {tmp[PLATFORM]} \033[1;31;40m")
                            print(f"  PORT: \033[1;32;40m {tmp[PORT]} \n")
                            foundFilePaths.append(tmp[FILE])
                            x = x + 1
                            break       #break to prevent duplicate results
                except:
                    print('Some sort of error occured: ',  sys.exc_info()[0])  #TODO: Do proper error handling here

                    exploitFileContent.clear
                    exploitFILE.close
        else:
            print('Skipping ' + exploitsfilepath + '  Does not exist!')
    return foundFilePaths

############################MAIN##################################

commandArgs = sys.argv[1:]
c = 1

try:
    args, argvalue = getopt.getopt(commandArgs, unixOptions, gnuOptions)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for currentArg, currentValue in args:
    if currentArg in ("-d", "--deep"):  #TODO:errorcheck currentValue to make sure search string is not too short resulting in too much output
        results = deepsearch(currentValue.lower(), openCSV(SSPATH))
        while c != 0:
            if results is not None:  #this is hilarious
                print("(0 to Exit)------------>", end=' ')
                c = int(input())
                if c == 0:
                    sys.exit(0)
                if (os.path.isfile(SSPATH + results[c-1])) == True:
                    with open(SSPATH + results[c - 1], 'r') as exploitFILE:
                        textFile = exploitFILE.read()
                        print(textFile)
                        exploitFILE.close

