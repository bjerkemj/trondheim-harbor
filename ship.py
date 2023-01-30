import container
import containerStorage

import numpy as np
import pprint


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
        L = self.dimensions['L']
        W = self.dimensions['W']
        H = self.dimensions['H']
        self.boxes = [[[None for w in range(W)]
                       for l in range(L)] for h in range(H)]
        self.l = 0
        self.w = 0
        self.h = 0
        self.nextLoadingCoordinate = (self.h, self.l, self.w)
        self.containerLocations = {}  # key is ID, value is a list of locations
        # List of holes that should be filled by 20-feet containers. Elements in this list are the coordinates (h, l, w) of the holes.
        self.holesToFill = []

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

    def loadShip(self, containersList):
        assert len(self.containerLocations) == 0,\
            print('Only works for loading empty ships')
        for cIndex in range(len(containersList)):
            container = containersList[cIndex]
            if container.getSize() == 20:
                if len(self.listOfHoles) > 0:
                    containerLocation = self.listOfHoles.pop(0)
                    self.containerLocations[container.getId()]

    def printLevel(self, level: int):
        print('Level:', level)
        pprint.pprint(self.boxes[int])


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
    # --------- Fill 3x3x3 ship with 40feet containers
    dim = {'L': 3, 'W': 3, 'H': 3}

    containers = containers40[:8]
    # [print(c.getId()) for c in containers]
    ship = Ship(dim, '3by3ship')
    ship.loadShip(containers)

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
