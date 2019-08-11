import commonVar as common
import os
import configparser

# reading configuratiion file(s)
def readConfigFile():
    config=configparser.ConfigParser()

    # to chose an INI file in the current folder
    filesHere=os.listdir(common.project+"/")
    selected=[]
    for i in range(len(filesHere)):
        if filesHere[i].find('.INI')>0 or \
        filesHere[i].find('.ini')>0: selected.append(filesHere[i])
        selected.sort()
    if len(selected) > 1:
        for i in range(len(selected)):
            print (i, selected[i])

    # if more than one INI file has to be read, simply repeat che code below
    num = 0
    if len(selected) > 1: num=int(input("Choose a file via its number (>=0;<="+\
                              str(len(selected)-1)+") "))
    print("parsing", selected[num])

    config.read(common.project+"/"+selected[num])

    # parameter setting (using get, getint, getfloat)
    common.mySeed       = config['project'].getint('mySeed')
    common.nAgents      = config['project'].getint('nAgents')
    common.nCycles      = config['project'].getint('nCycles')
    common.toBeExecuted = config['project'].get('toBeExecuted')


    #if len(selected)==1
