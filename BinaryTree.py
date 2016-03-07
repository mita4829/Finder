
class BinaryTree(object):
    def __init__(self, value=None, id=None, leftLeaf=0, rightLeaf=0):
        self.value = value
        self.id = id
        self.leftLeaf = leftLeaf
        self.rightLeaf = rightLeaf
    def getValue(self):
        return self.value
    def getLeftLeaf(self):
        return self.leftLeaf
    def getRightLeaf(self):
        return self.rightLeaf
    def setLeftLeaf(self,leftLeaf):
        self.leftLeaf = leftLeaf
    def setRightLeaf(self,rightLeaf):
        self.rightLeaf = rightLeaf


head = BinaryTree(5,"token",None,None)

def appendLeaf(head,leaf):
    if(leaf.getValue() > head.getValue()):
        if(head.getRightLeaf() == None):
            head.setRightLeaf(leaf)
            return
        head = head.getRightLeaf()
        appendLeaf(head,leaf)
    else:
        if(head.getLeftLeaf() == None):
            head.setLeftLeaf(leaf)
            return
        head = head.getLeftLeaf()
        appendLeaf(head,leaf)

def newLeaf(input):
    leaf = BinaryTree(valueFunction(input))

def printTree(head):
    if(head == None):
        return
    printTree(head.getLeftLeaf())
    print(str(head.getValue())+" ")
    printTree(head.getRightLeaf())

l = BinaryTree(3,"token",None,None)
r = BinaryTree(7,"token",None,None)
lr = BinaryTree(4,"token",None,None)
ll = BinaryTree(1,"token",None,None)


appendLeaf(head,l)
appendLeaf(head,r)
appendLeaf(head,lr)
appendLeaf(head,ll)

printTree(head)

def valueFunction(input):
    sum = 0
    for i in range(0,len(input)):
        sum = sum+ord(input[i])*i
    return sum

















#make sure onload that head cannot be null
#come up with a plan to handle node collisions