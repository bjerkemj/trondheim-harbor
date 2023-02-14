# 0. Imported modules and additional information
# ----------------------------------------------
from container import Container, createRandomContainers, doesSizeExist
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
print(ROOT)

# 1. ContainerStorage
# -------------------


class ContainerStorage:
    def __init__(self):
        self.containers = []

    def addContainer(self, container):
        self.containers.append(container)

    def addContainers(self, containers):
        for container in containers:
            self.addContainer(container)

    def removeContainer(self, containerId):
        container = self.findContainer(containerId)
        if container == None:
            raise Exception("There is no such container")
        self.containers.remove(container)

    def findContainer(self, containerId):
        for container in self.containers:
            if container.id == containerId:
                return container
        return None

    def removeAllContainers(self):
        self.containers = []

    def saveToFile(self, filename="containerSave"):
        with open(os.path.join(ROOT, filename + ".tsv"), "w") as f:
            f.write("ID SIZE WEIGHT CAPACITY LOAD \n")
            for container in self.containers:
                f.write(container.getId() + "\t")
                f.write(str(container.getSize()) + "\t")
                f.write(str(container.getWeight()) + "\t")
                f.write(str(container.getCapacity()) + "\t")
                f.write(str(container.getLoad()) + "\t")
                f.write("\n")

    def readFromFile(self, filename="containerSave"):
        self.removeAllContainers()
        with open(os.path.join(ROOT, filename + ".tsv"), "r") as f:
            f.readline()
            for line in f:
                containerInfo = line.split("\t")
                container = Container(
                    int(containerInfo[1]), containerInfo[0], int(containerInfo[4]))
                self.addContainer(container)

    def print(self):
        for container in self.containers:
            container.print()


# 2. Main
# -------

if __name__ == '__main__':
    p1 = ContainerStorage()
    p1.addContainers(createRandomContainers(5))
    p1.print()
    p1.saveToFile()
    p1.readFromFile()
