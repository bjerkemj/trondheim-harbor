from containerStack import ContainerStack
from container import Container

class ShipSection:
    def __init__(self, sectionID: int, width: int, length: int, maxStackHeight):
        self.freeContainerStacks = []
        self.fullContainerStacks = []
        self.width = width
        self.length = length
        self.maxStackHeight = maxStackHeight
        self.sectionID = sectionID
        self.totalWeight = 0
        self.maxStackHeight = maxStackHeight
        for w in range(width):
            for l in range(length):
                self.freeContainerStacks.append(ContainerStack(
                    sectionID, (w, l), maxStackHeight))
        self.full = len(self.freeContainerStacks) == 0

    def getAllStacks(self) -> list[ContainerStack]:
        return self.freeContainerStacks + self.fullContainerStacks

    def getSectionId(self) -> int:
        return self.sectionID
    
    def getWidth(self) -> int:
        return self.width
    
    def getLength(self) -> int:
        return self.length
    
    def getMaxStackHeight(self) -> int:
        return self.maxStackHeight

    def updateSectionWeight(self) -> None:
        self.totalWeight = sum([containerStack.getTotalWeight() for containerStack in self.getAllStacks()])

    def getLowestWeightContainerStack(self) -> ContainerStack:
        containerStackWeights = [stack.getTotalWeight()
                                 for stack in self.freeContainerStacks]
        return self.freeContainerStacks[containerStackWeights.index(min(containerStackWeights))]

    def isFull(self) -> bool:
        self.full = len(self.freeContainerStacks) == 0
        return self.full

    def addContainerToSection(self, containerList) -> None:
        if self.full:
            raise Exception(
                'This section is full. No more containers may be loaded')
        else:
            containerStack = self.getLowestWeightContainerStack()
            containerStack.addContainer(containerList)
            if (containerStack.isFull()):
                self.freeContainerStacks.remove(containerStack)
                self.fullContainerStacks.append(containerStack)
                self.isFull()
            self.updateSectionWeight()

    def getSectionWeight(self) -> int:
        return self.totalWeight

    def getNumOperationsInSection(self) -> int:
        return sum([containerStack.getNumOperations() for containerStack in self.getAllStacks()])
    
    def lookForContainer(self, id: str) -> bool:
        for stack in self.getAllStacks():
            if stack.lookForContainer(id):
                return True
        return False
    
    def removeContainer(self, id: str) -> list[Container]:
        if not self.lookForContainer(id):
            return None
        for stack in self.getAllStacks():
            if stack.lookForContainer(id):
                return stack.removeContainer(id)
    
    def emptySection(self) -> list[Container]:
        containers = []
        for stack in self.getAllStacks():
            containers += stack.emptyStack()
        return containers

 
    def getStack(self, tuple: tuple) -> ContainerStack:
        for stack in self.getAllStacks():
           if stack.getLocation() == tuple:
                return stack 
        
    def setStack(self, tuple: tuple, newStack: ContainerStack) -> None:
        for stack in self.freeContainerStacks:
            if stack.getLocation() == tuple:
                self.freeContainerStacks.remove(stack) 
        for stack in self.fullContainerStacks:
            if stack.getLocation() == tuple:
                self.fullContainerStacks.remove(stack)
        if newStack.isFull():
            self.fullContainerStacks.append(newStack)
        else:
            self.freeContainerStacks.append(newStack)
        self.updateSectionWeight()

    def countContainers(self):
        count=0
        for stack in self.getAllStacks():
            count+=stack.countContainers()
        return count
