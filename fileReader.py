import os
import logextractor
def openFolder(folder = "logs/orginalLogs"): # for sample
    os.chdir(folder)
    filesLst = os.listdir()
    print(filesLst)
    for file in filesLst:
        log = readFile(file)
        logextractor.logExtractor(log)

def readFile(fileName):
    file = open(fileName,"r")
    log = file.read()
    file.close()
    return log

def openFolderForFeatures(folder = "logs/samples"): # for sample
    os.chdir(folder)
    filesLst = os.listdir()
    for file in filesLst:
        log = readFile(file)
        logextractor.makeFeaturs(log)

