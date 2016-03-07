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

#Version 2.2 Bug fix where recursively locating logs can lead to improper parent folder naming, fixed through sanitation of the directory name.
#1/25/16 

#Version 3.0 New binary search tree data structure for optimized search speed when checking for duplications in O(log n) time.
#2/9/16

#Version 3.1 argparse library for handling command line arguments.

import os
import sys
import csv
import argparse
#import time


#Note: All leafs are nodes but not all nodes are leafs. Leafs do not have any children and are pointing to null or "none" for both left and right children.

#Nodes for the tree are in the format of (IDnum,Name,leftChild,rightChild)
class BinaryTree(object):
    def __init__(self, value=None, id=None, leftLeaf=0, rightLeaf=0):
        self.value = value
        self.id = id
        self.leftLeaf = leftLeaf
        self.rightLeaf = rightLeaf
        self.listOfFileNames = []
    def getValue(self):
        return self.value
    def getLeftLeaf(self):
        return self.leftLeaf
    def getRightLeaf(self):
        return self.rightLeaf
    def getID(self):
        return self.id
    def setValue(self,nodeValue):
        self.value = nodeValue
    def setID(self,idValue):
        self.id = idValue
    def setLeftLeaf(self,leftLeaf):
        self.leftLeaf = leftLeaf
    def setRightLeaf(self,rightLeaf):
        self.rightLeaf = rightLeaf

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
                
                leaf = createNewNode(checkForDuplicationLine)#create a new node
                if(appendLeaf(head,leaf)):#if true, that means the string does not exist.
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
                leaf = createNewNode(checkForDuplicationLine)#create a new node
                if(appendLeaf(head,leaf)):#if true, that means the string does not exist.
                    csvDataTransfer(object,self.parentName,self.name,trackSide,Track,Sector,Bad)

        token.close()

folderObjects = []
fileObjects = []
head = BinaryTree(0,None,None,None)

def main():
    #start = time.clock()
    #See if two arguments are supplied, else abort
    parser = argparse.ArgumentParser()
    parser.add_argument('InputDirectory',metavar='d', help='The directory of where the logs files are located.')
    parser.add_argument('OutputDirectory',metavar='o', help='The desired output directory along with desired output csv file name.')
    args = parser.parse_args()
    
    d = str(sys.argv[1])
    o = str(sys.argv[2])
    
    dropOffDirectory = findDropOffDirectory(o)
    reportName = checkSecondArgu(o)
    checkFirstArgu(d)


    print("\nInitializing objects...")
    try:
        objectFolder()
        print("Initialization successful\n")
    except:
        print("Initialization of folders and/or files failed. A possible cause for failure could be the script was pointed to the root directory of the computer in which the maximum recursion depth was exceeded while looking for logs. This is rare even if it's the case.")
        sys.exit()

    print("Extracting data from logs...")


    object = csvCreator(getCurrentDirectory(),dropOffDirectory,reportName)
    report = open(reportName, "r")
    dataObject = report.readlines()
    for i in range(0,len(fileObjects)):
        if((fileObjects[i].name).find(".log") != -1):
            fileObjects[i].extractData(object,dataObject)

    print("Extraction successful")
    print("A new csv file has been made")
    report.close()
 
#end = time.clock()
#print(end-start)
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


#Function to append a leaf to the tree. Returns false if a certain string already exist, true if it's new.
def appendLeaf(headNode,leaf):
    if(headNode.getID() == None):
        headNode = leaf
        return True
    if(leaf.getValue() > headNode.getValue()):
        if(headNode.getRightLeaf() == None):
            headNode.setRightLeaf(leaf)
            return True
        headNode = headNode.getRightLeaf() #If the current node's right child is not null, recursively call the function by passing in head's right child.
        return appendLeaf(headNode,leaf)
    elif(leaf.getValue() < headNode.getValue()):
        if(headNode.getLeftLeaf() == None):
            headNode.setLeftLeaf(leaf)
            return True
        headNode = headNode.getLeftLeaf() #If the current node's left child isn't null, recursively call the function with head's left child.
        return appendLeaf(headNode,leaf)
    else:
        if(leaf.getValue() == headNode.getValue() and leaf.getID() != headNode.getID()):
            for i in range(0,len(headNode.listOfFileNames)):
                if(headNode.listOfFileNames[i].getID() == leaf.getID()):
                    return False
            headNode.listOfFileNames.append(leaf) #If appending and a collision happend, add the node to the array
            return True
        else:
            return False


#Function for creating new nodes. The function first takes a string, perhaps from a file and hashes it for an integer from calling valueFunction(s). With it, a new node object will be made and will be appened to the tree.
def createNewNode(input):
    hashValue = hashFunction(input)
    node = BinaryTree(hashValue,input,None,None)
    if(head.getID() == None):
        head.setID(node.getID())
    return node


#Hash function. Equation: Sum up each char by their ASCII value and each char will be multipled by the current for loop index to make the hash as unique as possible even if two strings differ just from one char.
def hashFunction(input):
    sum = 0
    for i in range(0,len(input)):
        sum = sum+ord(input[i])*i
    return sum




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
#Function for printing the content of the tree in-order given the head node. If a node has no collisions, it will only print out the string name of the node, otherwise, it will loop through the node's array and print out all names. A node with the same hash value in an array will be denoted with a ++
def printTree(head):
    if(head == None):
        return
    printTree(head.getLeftLeaf())
    if(len(head.listOfFileNames) == 0):
        print(str(head.getID())+" ")
    else:
        print(str(head.getID())+" ")
        for i in range(0,len(head.listOfFileNames)):
            print(str(head.listOfFileNames[i].getID())+" "+"++")
    printTree(head.getRightLeaf())




main()
