from container import Container
from shipSection import ShipSection

import numpy as np
import random


class Ship2:

    """ A class representing a ship that can be loaded with 20- and 40-feet containers. The ship is divided into 6 equally sized sections,
     where section 0 and 1 is a the bow, 2 and 3 is the middle, and 4 and 5 is the stern. Odd number is starboard (right) and even is port (left). """
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
        sectionWidth = self.width/2
        sectionLength = self.length/3
        maxHeight = self.height
        for i in range(6):
            self.freeSections.append(ShipSection(
                i, sectionWidth, sectionLength, maxHeight))
        self.full = len(self.freeSections) == 0

    def isFull(self) -> bool:
        pass

    def updateShipWeight(self) -> None:
        pass

    def isShipBalanced(self) -> bool:
        pass


def main():
    pass


if __name__ == '__main__':
    main()
