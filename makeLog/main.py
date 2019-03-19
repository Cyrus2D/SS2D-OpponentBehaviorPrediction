from makeLog import fileReader
import os
fileReader.openFolder()
os.chdir("../")
fileReader.openFolderForFeatures()

# for debugging NueralNetwork
# fileReader.openFolder("testLog/orginalLogs")
# os.chdir("../../")
# fileReader.openFolderForFeatures("testLog/samples")

