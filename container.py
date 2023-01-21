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

class Container:
    def __init__(self, size, id = "XXX"):
        if not doesSizeExist(size):
            raise Exception("Invalid container size")
        self.id = id
        self.size = size                           # Size of container          (feet)
        self.weight = getContainerWeight(size)     # Weight of container        (tons)
        self.capacity = getContainerCapacity(size) # How much load you can fill (tons)
        self.load = 0                              # How much is loaded in cont.(tons)

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
    

    def myfunc(self):
        print("Size: " + str(self.size) + " feet \nInitial weight: " + str(self.weight) + " tons \nLoading capacity: " + str(self.capacity) + " tons \nLoad: " + str(self.load) + " \nId: " + str(self.id) + "\n")

def createRandomContainer():
    size = containerInfos[random.randint(0,len(containerInfos)-1)]["size"]
    container =  Container(size, createContainerId())
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
        id += str(random.randint(0,9))
    return id
# p1 = Container(20, "Pst")
# p1.myfunc()

createRandomContainers(5)