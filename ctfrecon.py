import sys, os

###CSV Identifiers###
ID = 0
FILE = 1
DESCRIPTION = 2
DATE = 3
AUTHOR = 4
TYPE = 5
PLATFORM = 6
PORT = 7
#####################
SSPATH = '/usr/share/exploitdb/' #searchsploit root dir

if len(sys.argv) > 1:
    squery = ' '.join(sys.argv[1:])
else:
    print('What are you looking for? ')
    squery = input()

if squery == '':
    print('Search query cannot be empty')
    sys.exit

#open, read all lines into list, and error check exploits CSV
if os.path.isfile(SSPATH + 'files_exploits.csv') == True:
    exploitCSV = open(SSPATH + 'files_exploits.csv')
    exploitlist = exploitCSV.readlines()
else:
    print(exploitspath + ' does not exist!')
    sys.exit

print("\n------------------------>SEARCH QUERY: " + squery)
squery = squery.lower()  #change to lowercase for matching

#parse lines
for line in exploitlist[1:]:
    line.strip('/n')
    tmp = line.split(',')
    exploitsfilepath = SSPATH + tmp[FILE]
    if os.path.isfile(exploitsfilepath) == True:
        with open(exploitsfilepath, 'r') as exploitFILE:
            try:
                exploitFILEcontent = exploitFILE.readlines()
                for contentLine in exploitFILEcontent:
                    contentLine = contentLine.lower()
                    search = contentLine.find(squery)
                    if search != -1:
                            print(f"\033[1;31;40m FILE: \033[1;32;40m {tmp[FILE]} \033[1;31;40m DESCRIPTION: \033[1;32;40m {tmp[DESCRIPTION]}")
                            break #found in file, break to prevent duplicate listing
            except:
                print('Some sort of error occured: ',  sys.exc_info()[0])

        #reset and close file
        exploitFILEcontent.clear
        exploitFILE.close
    else:
        print('Skipping ' + exploitsfilepath + '  Does not exist!')


print("")
exploitCSV.close




