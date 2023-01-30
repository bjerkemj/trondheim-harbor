import container
import containerStorage

import numpy as np
import pprint
import random


class Ship:
    defaultDimensions = {"L": 23, "W": 22, "H": 18}

    """ The bays/boxes is representer by a 3-d array where the outermost array is the height (from 0=floor level to level H-1),
    the second array is the position from the bow (front of the ship) (0 is at the 1st row, L-1 is the last row, aka at the bow)
     and the innermost array is the position from left to right (0 is all the way left, W-1 is all the way right).

    So the place (1, 2, 3) would mean the the second plane in height, and the following
    coordinate in the  horsinotal plane (marked by O). 

    A 20-feet ship takes one spot while a 40-feet takes two spots. All 40-feet ships are placed from left to right, NOT length-wise
    
    FRONT OF SHIP (BOW)
L   # # # # #   R
E   # # # # #   I
F   # # # O #   G
T   # # # # #   H
    # # # # #   T
    # # # # # 
    # # # # # 
    # # # # #
    BACK OF SHIP (STERN)
    
    
    
    Where the indexes are
    (0,0) (0,1) (0,2) ...
    (1,0) (1,1) (1,2) ... """

    def __init__(self, dimensions=defaultDimensions, shipID=None):
        if not shipID:
            shipID = self.generateShipID(dimensions)
        self.shipID = shipID
        self.dimensions = dimensions
        self.L = self.dimensions['L']
        self.W = self.dimensions['W']
        self.H = self.dimensions['H']
        self.boxes = [[[None for w in range(self.W)]
                       for l in range(self.L)] for h in range(self.H)]
        self.l = 0
        self.w = 0
        self.h = 0
        self.nextLoadingCoordinate = (self.h, self.l, self.w)
        self.containerLocations = {}  # key is ID, value is a list of locations
        # List of holes that should be filled by 20-feet containers. Elements in this list are the coordinates (h, l, w) of the holes.
        self.listOfHoles = []

    def generateShipId(self, capacity):
        # Johan
        pass

    def findContainer(self, containerID):
        # Naive solution, can optimize this once the rest of the logic is in place
        if not containerID in [self.containerLocations]:
            print(f"Container {containerID} is not in ship")
        else:
            containerLocationList = self.containerLocations[containerID]
            if len(containerLocationList) == 1:
                print(
                    f"Container found at location {containerLocationList[0]}")
            else:
                print(
                    f"Container found at locations {containerLocationList[0]} and {containerLocationList[1]}")

    def findAvailableSpot(self, container: container.Container):
        if container.getSize() == 40:
            self.findAvaialableSize40Spot(container)
        else:
            self.findAavailableSize20Spot(container)

    def findAavailableSize40Spot(self, container):
        # Need to check if we are on the edge. If we are on the edge then go to next available double spot
        pass

    def findAavailableSize20Spot(self, container):
        if len(self.listOfHoles) > 0:
            return self.listOfHoles.pop(0)
        return self.nextLoadingCoordinate

    def iterateCoordinate(self):
        if self.w < self.W - 1:  # Still room in width
            self.w += 1
        else:
            self.w = 0
            if self.l < self.L - 1:  # Still room in length
                self.l += 1
            else:
                self.l = 0
                if self.h < self.H - 1:  # Still room in height
                    self.h += 1
                else:
                    print('Ship is full')

    def loadShip(self, containersList):
        assert len(self.containerLocations) == 0,\
            print('Only works for loading empty ships')
        for cIndex in range(len(containersList)):
            container = containersList[cIndex]
            # self.printLevel(self.h)
            # print(f"Inserting container {container.getId()}")
            if container.getSize() == 20:
                if len(self.listOfHoles) > 0:
                    containerLocation = self.listOfHoles.pop(0)
                    self.containerLocations[container.getId()] = [(
                        containerLocation)]
                    self.boxes[containerLocation[0]][containerLocation[1]
                                                     ][containerLocation[2]] = container.getId()
                else:
                    self.containerLocations[container.getId()] = [
                        (self.h, self.l, self.w)]
                    self.boxes[self.h][self.l][self.w] = container.getId()
                    self.iterateCoordinate()
            else:  # container size is 40
                if self.w == self.W - 1:  # If we are on the rightmost edge, add this location as a hole and go to next row
                    self.listOfHoles.append((self.h, self.l, self.w))
                    self.iterateCoordinate()
                self.containerLocations[container.getId()] = [
                    (self.h, self.l, self.w)]
                self.boxes[self.h][self.l][self.w] = container.getId()
                self.iterateCoordinate()
                self.containerLocations[container.getId()].append(
                    (self.h, self.l, self.w))
                self.boxes[self.h][self.l][self.w] = container.getId()
                self.iterateCoordinate()

    def loadShipInDecreasingOrder(self, containersList: list):
        """ The weight of a container is considered as weight per 20-feet unit size, such that a 20-feet container weighing 5 tons is considered heavier than a 40-feet container weighting 9 tons """
        sortIndexes = np.argsort([container.getTotalWeight()/2 if container.getSize() == 40 else container.getTotalWeight()
                                 for container in containersList])
        sortedContainerList = [containersList[index] for index in sortIndexes]
        decreasingWeightContainerList = sortedContainerList[::-1]
        # for cont in decreasingWeightContainerList:
        #     print(cont.getTotalWeight(), cont.getId())
        self.loadShip(decreasingWeightContainerList)

    def printLevel(self, level: int):
        print('Level:', level)
        pprint.pprint(self.boxes[level])


def main():
    # Generate lots of containers for testing
    size = 20
    containers20 = []
    for i in range(50):
        name = str(size) + ':' + str(i).zfill(3)
        containers20.append(container.Container(size, name))
    size = 40
    containers40 = []
    for i in range(50):
        name = str(size) + ':' + str(i).zfill(3)
        containers40.append(container.Container(size, name))

    # [print(c.getId()) for c in containers20]

    # Tests
    # ---- Test 1:
    # --------- Fill 3x3x3 ship with 9 40feet containers
    dim = {'L': 3, 'W': 3, 'H': 3}

    containers = containers40[:9]
    # [print(c.getId()) for c in containers]
    ship = Ship(dim, '3by3ship')
    ship.loadShip(containers)

    for level in range(dim['H']):
        ship.printLevel(level)

    # ---- Test 2:
    # --------- Fill 3x3x3 ship with 9 40-feet containers and 9 20-feet containers
    dim = {'L': 3, 'W': 3, 'H': 3}

    containers = containers40[:9] + containers20[:9]
    # [print(c.getId()) for c in containers]
    ship = Ship(dim, '3by3ship')
    ship.loadShip(containers)

    for level in range(dim['H']):
        ship.printLevel(level)

    # ---- Test 3:
    # --------- Fill 3x3x3 ship with between random containers of size 20 and 40, filling up the entire ship
    dim = {'L': 3, 'W': 3, 'H': 3}
    numSpotsFilled = 0
    containers = []
    num20containers = 0
    num40containers = 0
    while numSpotsFilled < 3*3*3:
        if numSpotsFilled == 26:
            containers.append(containers20.pop(0))
            numSpotsFilled += 1
            num20containers += 1
        else:
            rndInt = random.randint(1, 2)
            if rndInt == 1:
                containers.append(containers20.pop(0))
                numSpotsFilled += 1
                num20containers += 1
            else:
                if num40containers == 9:  # not room for more than 8 containers in ship
                    continue
                containers.append(containers40.pop(0))
                numSpotsFilled += 2
                num40containers += 1
    # [print(c.getId()) for c in containers]
    ship = Ship(dim, '3by3ship')
    ship.loadShip(containers)

    for level in range(dim['H']):
        ship.printLevel(level)
    print(
        f'#20-feet containers = {num20containers}\n#40-feet containers = {num40containers}')
    # print(ship.containerLocations)

    # ---- Test 4:
    # --------- Fill 3x3x3 ship with 9 40-feet containers and 9 20-feet containers and load them by weight
    dim = {'L': 3, 'W': 3, 'H': 3}

    containers = containers40[:9] + containers20[:9]
    for cont in containers:
        rndLoad = random.randint(0, cont.getCapacity())
        cont.setLoad(rndLoad)
    # [print(c.getId()) for c in containers]
    ship = Ship(dim, '3by3ship')
    print('ContainerList unsorted: ')
    for cont in containers:
        print(cont.getTotalWeight(), cont.getId())
    print('ContainerList as loaded: ')
    ship.loadShipInDecreasingOrder(containers)

    # for level in range(dim['H']):
    #     ship.printLevel(level)

    # ship.boxes[0][0][0] = '000'
    # ship.boxes[0][0][1] = '001'
    # ship.boxes[0][2][1] = '021'
    # ship.boxes[0][2][2] = '022'

    # print(len(ship.boxes))
    # print(len(ship.boxes[0]))
    # print(len(ship.boxes[0][0]))

    # print('Base level:')
    # pprint.pprint(ship.boxes[0])


if __name__ == '__main__':
    main()
