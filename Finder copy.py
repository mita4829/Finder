#Michael Tang
#Version 1.0
#2/6/15
#Script to output bad sector data to a csv file

#Version 2.0 Now object-oriented
#10/27/15

#Version 2.1 Handles two arguments in the command line
#12/2/15

#Version 2.1.1 Handles two arguments in the command line
#1/12/16

#Version 2.2 Bug fix where recursively locating log can lead to improper parent naming. This was fix through sanitation of the directory name.
#1/25/16

import os
import sys
import csv

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
        print("\nHow to run: python3 Finder.py -d -o\n")
        print("-d Is the directory of where the folder of logs files are located. \n Example: '/Users/Guest/Desktop/FolderOfLogs' \n")
        print("-o Is the output directory and the desired name. \n Example: '/Users/Guest/Desktop/MyReport.csv' This will place the completed file on the Desktop and it will be called MyReport.csv\n")
        checkForHelp()
        sys.exit("\nScript aborted")
    dropOffDirectory = findDropOffDirectory(o)
    reportName = checkSecondArgu(o)
    checkFirstArgu(d)


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
    printString()
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
            object = File(token,getCurrentDirectory(),sanitizeLocalString(getCurrentDirectory()))
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

#check if user needs help
def checkForHelp():
    print("Finder.py produces a new .csv file and populates the file with data given log files. How to run the script. The script takes two arguments, the first, the directory of where the folder of log files are at. The second argument is where to place the newly made .csv file and what to name it. By defualt, it will be called 'Report.csv' unless specified.\n The arguments can handle both absolute directories and relative directories.\nExample: If you are on the Desktop where the Finder.py script is and there is a folder of logs on the Desktop called 'folderLogs', you can run the script by typing 'python3 Finder.py folderLogs MyReport.csv' in the shell.\n For the second argument, likewise to the first, it can take absolute and relative directories. If no directory is given, the placement of the .csv file will be the first argument, but, a name of what to call the .csv file MUST be given.\n Example: Consider the first example environment, when the script is finished, the new .csv file will be placed in the 'folderLogs' folder and it will be called 'newCSV.csv' by running this command in the shell 'python3 Finder.py folderLogs folderLogs/newCSV.csv'.")

#check first argument to see if it's an absolute or relative directory
def checkFirstArgu(d):
    try:
        s = str(getCurrentDirectory())
        if(d.find(s) != -1):
            changeDirectoryAnywhere(d)
        else:
            changeDirectory(d)
    except:
        print("Unable to navigate to "+d+" script aborted")
        sys.exit()

#check second argument to see if it's an absolute or relative directory and what to name the file
def checkSecondArgu(o):
    dropOffDirectory = getCurrentDirectory()
    reportName = "Report.csv"
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
    return reportName

def findDropOffDirectory(o):
    dropOffDirectory = getCurrentDirectory()
    reportName = "Report.csv"
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
    return dropOffDirectory

def sanitizeLocalString(input):
    last = -1;
    for i in range(0, len(input)):
        if(input[i] == "/"):
            last = i
    return input[last+1:len(input)]

#debugging functions
def printFolderObjects():
    print("----------Debug----------")
    for i in range(0,len(folderObjects)):
        print(folderObjects[i].name)
    print("-------------------------")
def printFileObjects():
    print("----------Debug----------")
    for i in range(0,len(fileObjects)):
        print(fileObjects[i])
    print("-------------------------")
def printString():
    print("----------Debug----------")
    for i in range(0,len(reportStrings)):
        print(reportStrings[i])
    print("-------------------------")

main()
