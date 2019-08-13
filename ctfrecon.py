import sys, os

exploitspath = '/usr/share/exploitdb/files_exploits.csv'
#shellcodespath = '/usr/share/exploitdb/files_shellcodes.csv'

if len(sys.argv) > 1:
    squery = ' '.join(sys.argv[1:])
else:
    print('What are you looking for? ')
    squery = input()

if squery == '':
    print('Search query cannot be empty')
    sys.exit

#open, read all lines into list, and error check exploits CSV
if os.path.isfile(exploitspath) == True:
    exploitCSV = open(exploitspath)
    exploitlist = exploitCSV.readlines()
else:
    print(exploitspath + ' does not exist!')
    sys.exit

print('Search Query: ' + squery)
squery = squery.lower()

#parse lines
for line in exploitlist:
    line.strip('/n')
    tmp = line.split(',')
    exploitsfilepath = '/usr/share/exploitdb/' + tmp[1]
    #print('Trying ' + exploitsfilepath + '...')   #verbose for debugging
    if os.path.isfile(exploitsfilepath) == True:
        with open(exploitsfilepath, 'r') as exploitFILE:
            try:
                exploitFILEcontent = exploitFILE.readlines()
                for contentLine in exploitFILEcontent:
                    contentLine = contentLine.lower()
                    search = contentLine.find(squery)
                    if search != -1:
                        print('FOUND IT!: ' + tmp[1])
            except:
                print('Error opening: ' + exploitsfilepath)

        #reset and close file
        exploitFILEcontent.clear
        exploitFILE.close
    else:
        print('Skipping ' + exploitsfilepath + '  Does not exist!')


exploitCSV.close




