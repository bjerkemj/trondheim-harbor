# 0. Imported modules and helper functions
# ----------------------------------------

import random

size20 = {
    "size": 20,
    "weight": 2,
    "capacity": 20
}

size40 = {
    "size": 40,
    "weight": 4,
    "capacity": 22
}

containerInfos = [size20, size40]


def doesSizeExist(sizeInt):
    for info in containerInfos:
        if info["size"] == sizeInt:
            return True
    return False


def getContainerWeight(sizeInt):
    for info in containerInfos:
        if info["size"] == sizeInt:
            return info["weight"]
    raise Exception("Can't find the container size")


def getContainerCapacity(sizeInt):
    for info in containerInfos:
        if info["size"] == sizeInt:
            return info["capacity"]
    raise Exception("Can't find the container size")

# 1. Container
# ------------

class Container:
    def __init__(self, size, id, load=0):
        if not doesSizeExist(size):
            print(doesSizeExist(size))
            raise Exception("Invalid container size")
        self.id = id
        self.size = size
        self.weight = getContainerWeight(size)
        self.capacity = getContainerCapacity(size)
        self.load = load

    def getId(self):
        return self.id

    def getSize(self):
        return self.size

    def getWeight(self):
        return self.weight

    def getCapacity(self):
        return self.capacity

    def getLoad(self):
        return self.load

    def setLoad(self, loadInt):
        if loadInt > self.capacity:
            raise Exception("To big load")
        self.load = loadInt

    def getTotalWeight(self):
        return self.load + self.weight

    def print(self):
        print(str(self.size) + " " + str(self.id) + " " +
              str(self.weight) + " " + str(self.capacity) + " " + str(self.load) + ' ' + str(self.getTotalWeight()))

# 2. Random container functions
# -----------------------------

def createRandomContainer():
    size = containerInfos[random.randint(0, len(containerInfos)-1)]["size"]
    container = Container(size, createContainerId(), )
    container.setLoad(random.randint(0, container.getCapacity()))
    return container

def createRandomContainers(numberOfContainers):
    containers = []
    for i in range(numberOfContainers):
        containers.append(createRandomContainer())
    return containers

def createContainerId():
    id = "JTLU"
    for _ in range(6):
        id += str(random.randint(0, 9))
    return id

# 3. Main
# -------

if __name__ == '__main__':
    # Single container test
    print("Single container test")
    c1 = Container(20, "ID1", 5)
    print("ID1 = " + c1.getId())
    print("20 = " + str(c1.getCapacity()))
    print("5 = " + str(c1.getLoad()))
    print("7 = " + str(c1.getTotalWeight()))
    print("2 = " + str(c1.getWeight()))
    c1.print()
    c1.setLoad(20)
    print("20 = " + str(c1.getLoad()))
    print("22 = " + str(c1.getTotalWeight()))
    c2 = Container(40, "ID2", 7)
    c2.print()

    print()

    # Random container test
    random.seed(1)
    print("Random container test")
    r1 = createRandomContainer()
    r1.print()
    r1.setLoad(10)
    print("10 = " + str(r1.getLoad()))
    randomContainer = createRandomContainers(5)
    for container in randomContainer:
        container.print()
