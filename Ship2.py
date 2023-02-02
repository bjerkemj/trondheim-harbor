from container import Container

import numpy as np
import random


class Ship2:
    defaultDimensions = {"L": 24, "W": 22, "H": 18}

    def __init__(self, dimensions=defaultDimensions, shipID=None) -> None:
        self.dimensions = dimensions
        self.shipID = shipID
        self.height = dimensions['H']
        self.width = dimensions['W']
        self.length = dimensions['L']


def main():
    pass


if __name__ == '__main__':
    main()
