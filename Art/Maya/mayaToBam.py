import re
import os
import sys

fileList = []
tempFile = []
for arg in sys.argv:
    if os.path.exists(arg):
        fileList.append(arg)
    else:
        print "File " + arg + " does not exist"
        sys.exit

# Convert the requested Maya files to egg and dump them in the "eggs" folder
fileList.remove("mayaToBam.py")
for mayaFile in fileList:
    fileName = mayaFile.split('.')[0]
    os.system("maya2egg2008 " + mayaFile + " " + "../" + fileName + ".egg")

# Move to the eggs folder and edit them to get the correct texture location
os.chdir("../")

for eggFile in fileList:
    fileName = eggFile.split('.')[0] + ".egg"
    currentFile = open(fileName, 'r')

    tempFile = currentFile.readlines()

    currentFile.close()
    os.remove(fileName)
    currentFile = open(fileName, 'a')

    for line in tempFile:
        newLine = re.sub("../textures", "textures", line) 
        currentFile.write(newLine + "\n")

    currentFile.write("\n")
    currentFile.close()

    os.system("egg2bam " + fileName + " " + eggFile.split('.')[0] + ".bam")
    os.system("move " + fileName + " eggs/")
