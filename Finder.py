#Michael Tang
#Version 1.0
#2/6/15
#Script to output bad sector data to a csv file

#Version 2.0 Now object-oriented
#10/27/15

#Version 2.1 Handles two arguments in the command line
#12/2/15

#first argument, -d location of where to run the script against relative to the current directory
#secnod argument, -o where to output the csv, and what to name it

import os   #library for file and folder manipulation
import sys  #library for command line arguments and system 
import csv  #library for csv


class Folder:
    def __init__(self,name,homeDirectory):
        self.name = name
        self.homeDirectory = homeDirectory
    def getName(self):
        return self.nameP
    def getHomeDirectory(self):
        return self.homeDirectory

class File:
    def __init__(self,name,homeDirectory,parentName):
        self.name = name
        self.homeDirectory = homeDirectory
        self.parentName = parentName
    def getName(self):
        return self.name
    def getHomeDirectory(self):
        return self.homeDirectory
    def changeFileName(self,newName):
        location = self.getHomeDirectory()
        os.chdir(location)
        oldName, fileType = os.path.splitext(self.name)
        os.rename(self.name,newName+fileType)
    def extractData(self,object,report):
        location = self.getHomeDirectory()
        os.chdir(location)
        token = open(self.name, "r")
        pageOfdata = token.readlines()
        length = len(pageOfdata)
        for i in range(0,length):
            #filter here to see if the information is under or over the bad sector string
            #some log files have the information one line above the string where it says "Bad sector found". The first if() catches the upper string and the second if() catches the lower string to see where the info is located.
            badSectorExist = (pageOfdata[i].find("Bad sector found") != -1)
            lineOfData = pageOfdata[i]
            if(badSectorExist and (pageOfdata[i-1].find("<error>") != -1)):
                lineOfData = pageOfdata[i-1]
                #tackSide
                trackSide = lineOfData[0:8]
                if(trackSide.find(".0") != -1):
                    trackSide = "0"
                else:
                    trackSide = "1"
                #track
                trkLocation = lineOfData.find("trk:")+5
                trkComma = lineOfData.find(",",trkLocation)
                Track = lineOfData[trkLocation:trkComma]
                #sector
                secLocation = lineOfData.find("sec:")+5
                secComma = lineOfData.find(",",secLocation)
                Sector = lineOfData[secLocation:secComma]
                #bad
                badLocation = lineOfData.find("bad:")+5
                badComma = lineOfData.find(",",badLocation)
                Bad = lineOfData[badLocation:badComma]
                #prevent duplication
                checkForDuplicationLine = (self.parentName+" "+self.name+" "+trackSide+" "+Track+" "+Sector+" "+Bad)
                found = False
                for j in range(0,len(reportStrings)):
                    if(checkForDuplicationLine == reportStrings[j]):
                        found = True
                if(not found):
                    reportStrings.append(checkForDuplicationLine)
                    csvDataTransfer(object,self.parentName,self.name,trackSide,Track,Sector,Bad)
            #Lower line
            if(badSectorExist and (pageOfdata[i+1].find("<error>") != -1)):
                lineOfData = pageOfdata[i+1]
                #tackSide
                trackSide = lineOfData[0:8]
                if(trackSide.find(".0") != -1):
                    trackSide = "0"
                else:
                    trackSide = "1"
                #track
                trkLocation = lineOfData.find("trk:")+5
                trkComma = lineOfData.find(",",trkLocation)
                Track = lineOfData[trkLocation:trkComma]
                #sector
                secLocation = lineOfData.find("sec:")+5
                secComma = lineOfData.find(",",secLocation)
                Sector = lineOfData[secLocation:secComma]
                #bad
                badLocation = lineOfData.find("bad:")+5
                badComma = lineOfData.find(",",badLocation)
                Bad = lineOfData[badLocation:badComma]
                checkForDuplicationLine = (self.parentName+" "+self.name+" "+trackSide+" "+Track+" "+Sector+" "+Bad)
                found = False
                for j in range(0,len(reportStrings)):
                    if(checkForDuplicationLine == reportStrings[j]):
                        found = True
                if(not found):
                    reportStrings.append(checkForDuplicationLine)
                    csvDataTransfer(object,self.parentName,self.name,trackSide,Track,Sector,Bad)
        token.close()

folderObjects = []
fileObjects = []
reportStrings = []

def main():
    #See if two arguments are supplied, else abort
    try:
        d = str(sys.argv[1])
        o = str(sys.argv[2])
    except:
        print("Two arguments need to be supplied. How to run: python3 Finder.py -d -o")
        print("-d Is the directory of where the folder of logs files are located. \n Example: '/Users/Guest/Desktop/FolderOfLogs' ")
        print("-o Is the output directory and the desired name. \n Example: '/Users/Guest/Desktop/MyReport.csv' This will place the completed file on the Desktop and name it MyReport.csv")
        sys.exit("Script aborted")
    reportName = "Report.csv"
    dropOffDirectory = getCurrentDirectory()

    #try second argument ---------------
    if(o.find(str(getCurrentDirectory())) != -1):
        j = -1
        for i in range(0,len(o)):
            if(o[i] == '/'):
                j = i
        if(j+1 > 0):
            dropOffDirectory = o[0:j+1]
            if(o.find(".csv") != -1):
                reportName = str(o[j+1:len(o)])

    else:
        o = dropOffDirectory+"/"+o
        j = -1
        for i in range(0,len(o)):
            if(o[i] == '/'):
                j = i
        if(j+1 > 0):
            dropOffDirectory = o[0:j+1]
            if(o.find(".csv") != -1):
                reportName = str(o[j+1:len(o)])
    #end -------------------------------

    #try first argument ---------
    #Modifty for relative directory
    try:
        s = str(getCurrentDirectory())
        if(d.find(s) != -1):
            changeDirectoryAnywhere(d)
        else:
            changeDirectory(d)
    except:
        print("Unable to navigate to "+d+" script aborted")
        sys.exit()
    #end ------------------------



    print("\nInitializing objects...")
    try:
        objectFolder()
        print("Initialization successful\n")
    except:
        print("Initialization of folders and/or files failed")

    print("Extracting data from logs...")

    try:
        object = csvCreator(getCurrentDirectory(),dropOffDirectory,reportName)
        report = open(reportName, "r")
        dataObject = report.readlines()
        for i in range(0,len(fileObjects)):
            if((fileObjects[i].name).find(".log") != -1):
                fileObjects[i].extractData(object,dataObject)

        print("Extraction successful")
        print("A new csv file has been made")
        report.close()
    except:
        print("Extraction failed")


#csv creator
def csvCreator(currentWorkingDirectory,desiredDirectory,reportName):
    changeDirectoryAnywhere(desiredDirectory)
    object = csv.writer(open(reportName,"w"))
    object.writerow(["Folder","File Name","Side","Track","Sector","Bad",])
    #changeDirectoryAnywhere(currentWorkingDirectory)
    return object

#return current working directory
def getCurrentDirectory():
    return os.getcwd()

#returns a list of file names in the working directory
def getFilesInDirectory():
    listOfFiles = os.listdir(getCurrentDirectory())
    return listOfFiles

#change directory
def changeDirectory(index):
    newDirectory = str(getCurrentDirectory()+'/'+index)
    os.chdir(newDirectory)

def changeDirectoryAnywhere(index):
    newDirectory = str(index)
    os.chdir(newDirectory)

#return to previous directory
def returnToParent():
    os.chdir('..')

#returns an int of the size of files in the current working directory
def numberOfFiles():
    numOfFiles = len(os.listdir())
    return numOfFiles

#returns a bool to see if directory is a file or folder
def isdir(currentDirectory):
    return os.path.isdir(currentDirectory)

#start up menu
def startUp():
    userInput = input("How to use: \n 1) Place this file, 'Finder.py' with the rest of the folders that contain logs. \n 2) Run the script. (c)continue or (q)quit: ")
    if(userInput == 'c'):
        return
    else:
        sys.exit("Script aborted")

#initialize objects for folders
def objectFolder():
    numOfFiles = numberOfFiles()
    listOfFiles = getFilesInDirectory()
    for i in range(0, numOfFiles):
        token = str(listOfFiles[i])
        if(isdir(token)):
            object = Folder(token,getCurrentDirectory())
            folderObjects.append(object)
            objectFile(token)
        elif(not isdir(token)):
            object = File(token,getCurrentDirectory(),getCurrentDirectory())
            fileObjects.append(object)

#initialize objects for files
def objectFile(directory):
    changeDirectory(directory)
    numOfFiles = numberOfFiles()
    listOfFiles = getFilesInDirectory()
    for i in range(0, numOfFiles):
        token = str(listOfFiles[i])
        if(isdir(token) == False):
            object = File(token,getCurrentDirectory(),directory)
            fileObjects.append(object)
        else:
            objectFolder()#allow recursion
    returnToParent()

#Add data to the csv file
def csvDataTransfer(object,parentName,name,trackSide,Track,Sector,Bad):
    object.writerow([parentName,name,trackSide,Track,Sector,Bad])

#debugging functions
def printFolderObjects():
    print("----------Debug----------")
    for i in range(0,len(folderObjects)):
        print(folderObjects[i].name)
    print("-------------------------")
def printFileObjects():
    print("----------Debug----------")
    for i in range(0,len(fileObjects)):
        print(fileObjects[i].name)
    print("-------------------------")
def printString():
    print("----------Debug----------")
    for i in range(0,len(reportStrings)):
        print(reportStrings[i])
    print("-------------------------")
def hash(s):
    hashSum = 0
    for i in range(0,len(s)):
        hashSum = ord(s[i]) + i + hashSum
    print(hashSum % 31)

main()
