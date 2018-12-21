import os
from makeLog import logextractor


def openFolder(folder = "logs/orginalLogs"): # for sample
    os.chdir(folder)
    filesLst = os.listdir()
    n = len(filesLst)
    for file in filesLst:
        log = readFile(file)
        logextractor.logExtractor(log)
        print("s",n)
        n -= 1

def readFile(fileName):
    file = open(fileName,"r")
    log = file.read()
    file.close()
    return log

def openFolderForFeatures(folder = "logs/samples"): # for sample
    os.chdir(folder)
    filesLst = os.listdir()
    n = len(filesLst)
    for file in filesLst:
        log = readFile(file)
        logextractor.makeFeaturs(log)
        print("f",n)
        n -= 1
