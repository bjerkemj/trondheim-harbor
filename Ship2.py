from container import Container
from container import createRandomContainers
from shipSection import ShipSection

import numpy as np
import random

import time


class Ship2:

    """ A class representing a ship that can be loaded with 20- and 40-feet containers. The ship is divided into 6 equally sized sections,
     where section 0 and 1 is a the bow (front), 2 and 3 is the middle, and 4 and 5 is the stern (back). Odd number is starboard (right) and even is port (left). """
    defaultDimensions = {"L": 24, "W": 22, "H": 18}

    def __init__(self, dimensions=defaultDimensions, shipID=None) -> None:
        """ NB: Currently only works when L is divisble by 3 and W is divisible by 2 """
        self.dimensions = dimensions
        self.shipID = shipID
        self.height = dimensions['H']
        self.width = dimensions['W']
        self.length = dimensions['L']
        self.freeSections = []
        self.fullSections = []
        sectionWidth = int(self.width/2)
        sectionLength = int(self.length/3)
        maxHeight = self.height
        for i in range(6):
            self.freeSections.append(ShipSection(
                i, sectionWidth, sectionLength, maxHeight))
        self.full = len(self.freeSections) == 0
        self.holdingSpot = []  # Holding spot for a single 20-feet container

    def isFull(self) -> bool:
        return len(self.freeSections) == 0

    def updateShipWeight(self) -> None:
        pass

    def isShipBalanced(self) -> bool:
        pass

    def getLowestWeightShipSection(self) -> ShipSection:
        shipSectionWeights = [shipSection.getSectionWeight()
                              for shipSection in self.freeSections]
        return self.freeSections[shipSectionWeights.index(min(shipSectionWeights))]

    def addContainer(self, container: Container) -> None:
        if self.isFull():
            raise Exception('Ship is full, no more containers may be added')
        lowestWeightSection = self.getLowestWeightShipSection()
        if container.size == 20:
            if self.holdingSpot:
                containers = [self.holdingSpot.pop(), container]
                lowestWeightSection.addContainerToSection(containers)
            else:
                self.holdingSpot.append(container)
        else:
            lowestWeightSection.addContainerToSection(container)
        if lowestWeightSection.isFull():
            self.freeSections.remove(lowestWeightSection)
            self.fullSections.append(lowestWeightSection)

    def getNumberOfOperationsInShip(self) -> int:
        return sum([shipSection.getNumOperationsInSection()
                    for shipSection in self.freeSections]) + sum([shipSection.getNumOperationsInSection()
                                                                  for shipSection in self.fullSections])


def main():

    ship = Ship2()
    numContainers = 20000
    randomContainers = createRandomContainers(numContainers)
    numContainersAdded = 0
    start = time.time()
    try:
        for container in randomContainers:
            ship.addContainer(container)
            numContainersAdded += 1
    except Exception as e:
        print('Unable to load all containers. The following exception was thrown:')
        print(e)

    finally:
        end = time.time()
        print(numContainersAdded, 'added to ship')
        print(f'Script took {end - start:0f} seconds')
        print(
            f"Number of crane operations using a single crane was: {ship.getNumberOfOperationsInShip()}")


if __name__ == '__main__':
    main()
