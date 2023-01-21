# JLT U 123456 7
# JLT = owner of container
# U = eqiupment category identifier (u means all freight container)
# 123456 = serial number chosen by owner
# 7 = check digit (calculated by the other numbers with algorithm)
# http://www.gvct.co.uk/2011/09/how-is-the-check-digit-of-a-container-calculated/
# Here the check digit algo is written

from container import Container

class ContainerStorage:
    def __init__(self):
        self.containers = [] 

    def addContainer(self, container):
        self.containers.append(container)

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
    
    def myfunc(self):
        print(self.containers)
        print(self.removeContainer("pst"))
        print(self.containers)

cont = Container(20, "pst")
cont.myfunc()

p1 = ContainerStorage()
p1.addContainer(cont)
p1.myfunc()
