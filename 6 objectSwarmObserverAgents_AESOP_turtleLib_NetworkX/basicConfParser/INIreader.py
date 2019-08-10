import commonVar as common
import os
from configparser import ConfigParser

# reading configuratiion file(s)
def readConfigFile():
    # to chose an INI file in the current folder
    filesHere=os.listdir("./")
    selected=[]
    for i in range(len(filesHere)):
        if filesHere[i].find('.INI')>0 or \
        filesHere[i].find('.ini')>0: selected.append(filesHere[i])
        selected.sort()
        for i in range(len(selected)):
            print (i, selected[i])

        num=int(input("Choose a file via its number (>=0;<="+\
                str(len(selected)-1)+") "))
        print(selected[num])
