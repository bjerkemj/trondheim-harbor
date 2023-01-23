# JLT U 123456 7
# JLT = owner of container
# U = eqiupment category identifier (u means all freight container)
# 123456 = serial number chosen by owner
# 7 = check digit (calculated by the other numbers with algorithm)
# http://www.gvct.co.uk/2011/09/how-is-the-check-digit-of-a-container-calculated/
# Here the check digit algo is written

from container import Container, createRandomContainers
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
print(ROOT)


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

    def saveToFile(self, filename="standardSave"):
        print('----')
        f = open(os.path.join(ROOT, filename + ".tsv"), "w")
        f.write("ID SIZE WEIGHT CAPACITY LOAD \n")
        for container in self.containers:
            f.write(container.getId() + "\t")
            f.write(str(container.getSize()) + "\t")
            f.write(str(container.getWeight()) + "\t")
            f.write(str(container.getCapacity()) + "\t")
            f.write(str(container.getLoad()) + "\t")
            f.write("\n")
        f.write("---")
        f.close()

    def myfunc(self):
        print(self.containers)
        print(self.removeContainer("pst"))
        print(self.containers)


p1 = ContainerStorage()
p1.addContainers(createRandomContainers(5))
p1.saveToFile()
