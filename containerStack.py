from container import Container
import os
ROOT = os.path.dirname(os.path.abspath(__file__))


class ContainerStack:
    def __init__(self, section: int, loc: tuple, maxHeight: int) -> None:
        self.loc = loc
        self.maxHeight = maxHeight
        self.weight = 0
        self.topWeight = 0
        self.containers = []
        self.numOperations = 0

    def getContainers(self) -> list:
        return self.containers

    def countContainers(self) -> int:
        count = 0
        for containerList in self.containers:
            count += len(containerList)
        return count

    def getLocation(self) -> tuple:
        return self.loc

    def _updateTopWeight(self) -> None:
        if self.isEmpty():
            self.topWeight = 0
        else:
            self.topWeight = sum([container.getTotalWeight()
                                  for container in self.containers[-1]])

    def _pushContainer(self, containers: 'list[Container]') -> None:
        if self.isFull():
            raise Exception(
                'This containerStack is full -> unable to load another container')
        else:
            if type(containers) is Container:  # containers is one 40 feet container
                self.weight += containers.getTotalWeight()
                self.containers.append([containers])
                self.numOperations += 1
            else:  # containers is list of two 20 feet containers
                if len(containers) == 2:
                    for container in containers:
                        if container.getSize() == 40:
                            raise Exception(
                                'Only two 20-feet containers or 1 40-feet container may be loaded at the same time')
                        self.weight += container.getTotalWeight()
                    self.containers.append(containers)
                    self.numOperations += 2
                else:
                    self.weight += containers[0].getTotalWeight()
                    self.containers.append(containers)
                    self.numOperations += 1
            self._updateTopWeight()

    def addContainer(self, container: 'list[Container]') -> None:
        if type(container) is Container:
            if container.getSize() == 20:
                raise Exception(
                    'A single 20 foot container cannot be loaded to a containerStack')
            else:
                containerWeight = container.getTotalWeight()
                container = [container]
        else:
            if len(container) == 1:
                containerWeight = container[0].getTotalWeight()
            else:  # container is a list of two Containers
                for c in container:
                    containerWeight = 0
                    if c.getSize() == 40:
                        raise Exception(
                            'Only two 20-feet containers or 1 40-feet container may be loaded at the same time')
                    containerWeight += c.getTotalWeight()
        tempStack = []
        while containerWeight > self.topWeight and self.topWeight != 0:  # Pop all lighter containers from stack
            tempStack.append(self.popContainer())
        tempStack.append(container)
        while len(tempStack) > 0:  # Add containers again in decreasing weight order
            self._pushContainer(tempStack.pop())

    def addContainerFourCranes(self, container: 'list[Container]') -> int:
        operations = 0
        if type(container) is Container:
            if container.getSize() == 20:
                raise Exception(
                    'A single 20 foot container cannot be loaded to a containerStack')
            else:
                containerWeight = container.getTotalWeight()
                container = [container]
        else:
            if len(container) == 1:
                containerWeight = container[0].getTotalWeight()
            else:  # container is a list of two Containers
                for c in container:
                    containerWeight = 0
                    if c.getSize() == 40:
                        raise Exception(
                            'Only two 20-feet containers or 1 40-feet container may be loaded at the same time')
                    containerWeight += c.getTotalWeight()
        tempStack = []
        while containerWeight > self.topWeight and self.topWeight != 0:  # Pop all lighter containers from stack
            if(len(container) == 2):
                operations += 2
            else:
                operations += 1
            tempStack.append(self.popContainer())
        tempStack.append(container)
        while len(tempStack) > 0:  # Add containers again in decreasing weight order
            self._pushContainer(tempStack.pop())
            if(len(container) == 2):
                operations += 2
            else:
                operations += 1
        return operations

    def removeContainer(self, id: str) -> 'list[Container]':
        if not self.lookForContainer(id):
            return None

        tempStack = []
        found = False

        while not found:
            containerList = self.popContainer()
            if len(containerList) == 2:
                if containerList[0].getId() == id or containerList[1].getId() == id:
                    found = True
                else:
                    tempStack.append(containerList)
            else:
                if containerList[0].getId() == id:
                    found = True
                else:
                    tempStack.append(containerList)

        while len(tempStack) > 0:
            self._pushContainer(tempStack.pop())
        return containerList

    def lookForContainer(self, id: str) -> bool:
        for containerList in self.containers:
            for container in containerList:
                if container.getId() == id:
                    return True
        return False

    def getTotalWeight(self) -> int:
        return self.weight

    def getAverageWeight(self) -> float:
        return self.getTotalWeight()/self.getHeight()

    def getTopWeight(self) -> int:
        return self.topWeight

    def popContainer(self) -> 'list[Container]':
        if not self.isEmpty():
            popped_containers = self.containers.pop()
            lost_weight = sum([container.getTotalWeight()
                              for container in popped_containers])
            self.weight -= lost_weight
            self._updateTopWeight()
            self.numOperations += len(popped_containers)
            return popped_containers
        else:
            raise Exception("Can't pop from an empty container")

    def emptyStack(self) -> int:
        containers = []
        while not self.isEmpty():
            poppedContainers = self.popContainer()
            for container in poppedContainers:
                containers.append(container)
        return containers

    def isEmpty(self) -> bool:
        return len(self.containers) == 0

    def isFull(self) -> bool:
        return len(self.containers) == self.maxHeight

    def getHeight(self) -> int:
        return len(self.containers)

    def peek(self) -> list:
        """ Returns a list of container(s) at the top of the containerStack.
        If the containerStack is empty, throw error """
        if self.isEmpty():
            raise Exception("Can't peek in empty stack")
        return self.containers[-1]

    def getNumOperations(self) -> int:
        return self.numOperations

    def saveToFile(self, filename: str = "containerStackSave") -> None:
        with open(os.path.join(ROOT, filename + ".tsv"), "w") as f:
            for containers in self.getContainers():
                for container in containers:
                    f.write(container.getId() + "\t")
                    f.write(str(container.getSize()) + "\t")
                    f.write(str(container.getWeight()) + "\t")
                    f.write(str(container.getCapacity()) + "\t")
                    f.write(str(container.getLoad()) + "\t")
                    f.write("-\t")

    def readFromFile(self, filename: str = "containerStackSave") -> None:
        listFor20Containers = []
        containers = []
        with open(os.path.join(ROOT, filename + ".tsv"), "r") as f:
            line = f.readline()
            rowInfo = line.split("-")
            for info in rowInfo:
                infoSplitted = info.strip("\n").strip("\t").split("\t")
                if(len(infoSplitted) == 1):
                    continue
                container = Container(
                    int(infoSplitted[1]), infoSplitted[0], int(infoSplitted[4]))
                if container.getSize() == 40:
                    containers.append([container])
                elif container.getSize() == 20 and listFor20Containers:
                    listFor20Containers.append(container)
                    containers.append(listFor20Containers)
                    listFor20Containers = []
                else:
                    listFor20Containers.append(container)
        self.containers = containers
