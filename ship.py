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
    
    # # # # # 
    # # # # #
    # # # O #
    # # # # #
    # # # # #
    # # # # # 
    # # # # # 
    # # # # #
    
    
    
    Where the indexes are
    (0,0) (1,0) (2,0) ...
    (1,0) (1,1) () """

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

    def generateShipId(self, capacity):
        # Johan
        pass

    def findContainer(self, containerID):
        locationOfContainer = []
        # Naive solution, can optimize this once the rest of the logic is in place
        if not containerID in self.containerLocations:
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
        # Need to check if we are on the edge. If we are on the edge
        pass

    def findAavailableSize40Spot(self, container):
        return self.nextLoadingCoordinate

    def loadShip(lis):
        pass


def main():
    testDimensions = {"L": 4, "W": 3, "H": 2}

    ship = Ship(dimensions=testDimensions, shipID='JA')

    ship.boxes[0][0][0] = '000'
    ship.boxes[0][0][1] = '001'
    ship.boxes[0][2][1] = '021'
    ship.boxes[0][2][2] = '022'

    print(len(ship.boxes))
    print(len(ship.boxes[0]))
    print(len(ship.boxes[0][0]))

    print('Base level:')
    pprint.pprint(ship.boxes[0])


if __name__ == '__main__':
    main()
