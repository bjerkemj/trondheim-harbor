from containerStack import ContainerStack


class ShipSection:

    """ A class resperesenting a segment of the ship.

    params:
    SectionID: int
        Section number
    containerStacks: list
        list of containerStacks within this section
    totalWeight: int
        The total weight of this Ship Section
    maxStackHeight: int
        the maximum height of the stacks in this ship
    width: int
        The width of the section
    length: int
        The length of the section
    freeContainerStacks: list
        A list of ContainerStacks that are not full
    fullContainerStacks: list
        A list of ContainerStacks 
    numStacks: int
        Number of stacks in this section
    full: boolean
        True if no more containers can be added to Section

    """

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

    def getSectionId(self) -> int:
        return self.sectionID
    
    def getWidth(self) -> int:
        return self.width
    
    def getLength(self) -> int:
        return self.length
    
    def getMaxStackHeight(self) -> int:
        return self.maxStackHeight

    def updateSectionWeight(self) -> None:
        self.totalWeight = sum([containerStack.getTotalWeight() for containerStack in self.freeContainerStacks]) + sum(
            [containerStack.getTotalWeight() for containerStack in self.fullContainerStacks])

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
        return sum([containerStack.getNumOperations() for containerStack in self.freeContainerStacks]) + sum([containerStack.getNumOperations() for containerStack in self.fullContainerStacks])
    
    def getStack(self, tuple: tuple) -> ContainerStack:
        for stack in self.freeContainerStacks:
            if stack.getLocation() == tuple:
                return stack
        for stack in self.fullContainerStacks:
            if stack.getLocation() == tuple:
                return stack
        
