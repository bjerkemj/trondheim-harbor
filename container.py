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


def doesSizeExist(sizeInt: int) -> bool:
    for info in containerInfos:
        if info["size"] == sizeInt:
            return True
    return False


def getContainerWeight(sizeInt: int) -> int:
    for info in containerInfos:
        if info["size"] == sizeInt:
            return info["weight"]
    raise Exception("Can't find the container size")


def getContainerCapacity(sizeInt: int) -> int:
    for info in containerInfos:
        if info["size"] == sizeInt:
            return info["capacity"]
    raise Exception("Can't find the container size")

# 1. Container
# ------------

class Container:
    def __init__(self, size: int, id: str, load: int =0):
        if not doesSizeExist(size):
            print(doesSizeExist(size))
            raise Exception("Invalid container size")
        self.id = id
        self.size = size
        self.weight = getContainerWeight(size)
        self.capacity = getContainerCapacity(size)
        self.load = load

    def getId(self) -> str:
        return self.id

    def getSize(self) -> int:
        return self.size

    def getWeight(self) -> int:
        return self.weight

    def getCapacity(self) -> int:
        return self.capacity

    def getLoad(self) -> int:
        return self.load

    def setLoad(self, loadInt: int) -> None:
        if loadInt > self.capacity:
            raise Exception("To big load")
        self.load = loadInt

    def getTotalWeight(self) -> int:
        return self.load + self.weight

    def print(self):
        print(str(self.size) + " " + str(self.id) + " " +
              str(self.weight) + " " + str(self.capacity) + " " + str(self.load) + ' ' + str(self.getTotalWeight()))

# 2. Random container functions
# -----------------------------

def createRandomContainer() -> Container:
    size = containerInfos[random.randint(0, len(containerInfos)-1)]["size"]
    container = Container(size, createContainerId(), )
    container.setLoad(random.randint(0, container.getCapacity()))
    return container

def createRandomContainers(numberOfContainers) -> list[Container]:
    containers = []
    for i in range(numberOfContainers):
        containers.append(createRandomContainer())
    return containers

def createContainerId() -> str:
    id = "JTLU"
    for _ in range(6):
        id += str(random.randint(0, 9))
    return id