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
    # ---------------------
    c1 = Container(20, "ID1", 5)
    assert c1.getId() == "ID1", \
        f"Container id  should be ID1 but was {c1.getId()}"
    assert c1.getCapacity() == 20, \
        f"Container capacity should be 20 but was {c1.getCapacity()}"
    assert c1.getLoad() == 5, \
        f"Container load should be 5 but was {c1.getLoad()}"
    assert c1.getTotalWeight() == 7, \
        f"Total container weight weight should be 7 but was {c1.getTotalWeight()}"
    assert c1.getWeight() == 2, \
        f"Container inherit weight should be 2 but was {c1.getWeight()}"

    c1.setLoad(20)
    assert c1.getLoad() == 20, \
        f"Container load should be 20 but was {c1.getLoad()}"
    assert c1.getTotalWeight() == 22, \
        f"Total container weight weight should be 22 but was {c1.getTotalWeight()}"

    c2 = Container(40, "ID2", 7)
    assert c2.getId() == "ID2", \
        f"Container id  should be ID2 but was {c2.getId()}"
    assert c2.getCapacity() ==  22, \
        f"Container capacity should be 22 but was {c2.getCapacity()}"
    assert c2.getLoad() == 7, \
        f"Container load should be 7 but was {c2.getLoad()}"
    assert c2.getTotalWeight() == 11, \
        f"Total container weight weight should be 11 but was {c2.getTotalWeight()}"
    assert c2.getWeight() == 4, \
        f"Container inherit weight should be 4 but was {c2.getWeight()}"

    # Random container test
    # ---------------------
    
    random.seed(1)
    print("Random container test")
    rc1 = createRandomContainer()
    assert isinstance(rc1, Container), \
        f"The object should be a container but was {type(c1).__name__}"
    rc1.setLoad(10)
    assert rc1.getLoad() == 10, \
        f"Container load should be 7 but was {rc1.getLoad()}"
    
    randomContainers = createRandomContainers(5)
    for container in randomContainers:
        assert isinstance(container, Container), \
            f"The object should be a container but was {type(container).__name__}"


