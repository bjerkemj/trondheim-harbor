from container import Container


class ContainerStack:

    """ 
    A class representing a stack of containers using list operations.

    params:
    section: int
        section number
    loc: tuple
        the location of the ContainerStack within the section, i.e (0, 0) is in the upper left corner
    maxHeight: int
        Maximum height (number of 40-feet container equivalents there is room for in the vertical direction) """

    def __init__(self, section: int, loc: tuple, maxHeight: int) -> None:
        self.loc = loc
        self.maxHeight = maxHeight
        self.weight = 0
        self.topWeight = 0
        self.containers = []

    def pushContainer(self, containers) -> None:
        """ Adds the container/containers to the top of the containerStack and updates the total containerStack weight and the containerStack topWeight

        args:
        container: Container or list
            container is either 1 40-feet container or a list containing two 20-feet containers  """
        if self.isFull():
            raise Exception(
                'This containerStack is full -> unable to load another container')
        else:
            if type(containers) is Container:
                if containers.getSize() == 20:
                    raise Exception(
                        'A single 20 foot container cannot be loaded to a containerStack')
                self.weight += containers.getTotalWeight()
                self.topWeight = containers.getTotalWeight()
                self.containers.append([container])
            else:
                self.topWeight = 0
                for container in containers:
                    if container.getSize() == 40:
                        raise Exception(
                            'Only two 20-feet containers or 1 40-feet container may be loaded at the same time')
                    self.weight += container.getTotalWeight()
                    self.topWeight += container.getTotalWeight()
                self.containers.append(containers)

    def getTotalWeight(self) -> int:
        return self.weight

    def getAverageWeight(self) -> float:
        return self.getTotalWeight()/self.getHeight()

    def getTopWeight(self) -> int:
        return self.topWeight

    def popContainer(self):
        if not self.isEmpty():
            return self.containers.pop()
        else:
            raise Exception("Can't pop from an empty container")

    def isEmpty(self) -> bool:
        return len(self.containers) == 0

    def isFull(self) -> bool:
        return len(self.containers) == self.maxHeight

    def getHeight(self) -> int:
        return len(self.containers)

    def peek(self):
        """ Returns a list of container(s) at the top of the containerStack.
        If the containerStack is empty, throw error """
        if self.isEmpty():
            raise Exception("Can't peek in empty stack")
        return self.containers[-1]


def main():
    stack = ContainerStack(0, (0, 0), 100)
    print(stack.peek())


if __name__ == '__main__':
    main()
