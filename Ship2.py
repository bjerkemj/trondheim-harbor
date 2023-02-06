from container import Container
from container import createRandomContainers
from shipSection import ShipSection

import numpy as np
import random
import os
import time
from typing import List

ROOT = os.path.dirname(os.path.abspath(__file__))


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
        sectionLength = int(self.length/6)
        maxHeight = self.height
        for i in range(6):
            self.freeSections.append(ShipSection(
                i, sectionWidth, sectionLength, maxHeight))
        self.full = len(self.freeSections) == 0
        self.holdingSpot = []  # Holding spot for a single 20-feet container

    def isFull(self) -> bool:
        return len(self.freeSections) == 0
    
    def getSection(self, sectionId) -> List[ShipSection]:
        for section in self.freeSections:
            if section.getSectionId() == sectionId:
                return section
        for section in self.fullSections:
            if section.getSectionId() == sectionId:
                return section

    def updateShipWeight(self) -> None: # Johan mener denne kan slettes?
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

    def getAllSections(self) -> List[ShipSection]:
        allSections = []
        for section in self.freeSections:
            allSections.append(section)
        for section in self.fullSections:
            allSections.append(section)
        return allSections

    def getTotalWeight(self) -> int:
        totalWeight = 0
        allSections = self.getAllSections()
        for section in allSections:
            totalWeight += section.getSectionWeight()
        return totalWeight
    
    def getTotalWeightStarboard(self) -> int:
        totalWeightStarboard = 0
        allSections = self.getAllSections()
        for section in allSections:
           if section.getSectionId() in [1,3,5]:
               totalWeightStarboard += section.getSectionWeight()
        return totalWeightStarboard
               
    def getTotalWeightPort(self) -> int:
        totalWeightPort = 0
        allSections = self.getAllSections()
        for section in allSections:
           if section.getSectionId() in [0,2,4]:
               totalWeightPort += section.getSectionWeight()
        return totalWeightPort

    def getTotalWeightSections(self) -> List[int]:
        sectionWeights = [0, 0, 0]
        allSections = self.getAllSections()
        for section in allSections:
            sectionId = section.getSectionId()
            if sectionId in [0,1]:
                sectionWeights[0] += section.getSectionWeight()
            elif sectionId in [2,3]:
                sectionWeights[1] += section.getSectionWeight()
            elif sectionId in [4,5]:
                sectionWeights[2] += section.getSectionWeight()
        return sectionWeights
    
    def isShipBalanced(self, x_perc=0.05, y_perc=0.1):
        weightPortside = self.getTotalWeightPort()
        weightStarboard = self.getTotalWeightStarboard()
        weightSection = self.getTotalWeightSections()

        if weightPortside > weightStarboard * (1 + x_perc):
            print("Port side to heavy")
            return False

        if weightPortside < weightStarboard * (1 - x_perc):
            print("Starboard to heavy")
            return False
        
        if weightSection[1] > weightSection[0] * (1 + y_perc) or weightSection[2] > weightSection[0] * (1 + y_perc):
            print("Mid or stern section to heavy")
            return False

        if weightSection[0] > weightSection[1] * (1 + y_perc) or weightSection[2] > weightSection[1] * (1 + y_perc):
            print("Bow or stern section to heavy")
            return False

        if weightSection[0] > weightSection[2] * (1 + y_perc) or weightSection[1] > weightSection[2] * (1 + y_perc):
            print("Bow or mid section to heavy")
            return False 

        print("The ship is loaded correctly")
        return True
    
    def saveToFile(self, filename="shipSave"):
            with open(os.path.join(ROOT, filename + ".tsv"), "w") as f:
                allSections = self.getAllSections()
                for section in allSections:
                    f.write("Section: " + str(section.getSectionId()) + "\n")
                    width = section.getWidth()
                    length = section.getLength()
                    for l in range(length):
                        for w in range(width):
                            for containers in section.getStack((w,l)).getContainers():
                                for container in containers:
                                    f.write(container.getId() + "\t")
                                    f.write(str(container.getSize()) + "\t")
                                    f.write(str(container.getWeight()) + "\t")
                                    f.write(str(container.getCapacity()) + "\t")
                                    f.write(str(container.getLoad()) + "\t")
                                    f.write("-\t")
                            f.write("\n")

    def readFromFile(self, filename="shipSave"):
        with open(os.path.join(ROOT, filename + ".tsv"), "r") as f:
            sectionId = 0
            widthCounter = 0
            lengthCounter = 0
            listFor20Containers = []
            for line in f:
                if line.startswith("Section: "):
                    sectionId = int(line[9])
                    section = self.getSection(sectionId)
                    width = section.getWidth()
                    length = section.getLength()
                    continue
                stack = section.getStack((widthCounter, lengthCounter))
                rowInfo = line.split("-")
                for info in rowInfo:
                    infoSplitted = info.strip("\n").strip("\t").split("\t")
                    if(len(infoSplitted)==1):
                        continue
                    container = Container(int(infoSplitted[1]), infoSplitted[0], int(infoSplitted[4]))
                    if container.getSize==40:
                        stack.pushContainer([container])
                    elif container.getSize==20 and listFor20Containers:
                        listFor20Containers.append(container)
                        stack.pushContainer(listFor20Containers)
                        listFor20Containers = []
                    else:
                        listFor20Containers.append(container)
                widthCounter+=1
                if widthCounter == width:
                    widthCounter=0
                    lengthCounter+=1

def main():

    ship = Ship2()
    numContainers = 20000
    randomContainers = createRandomContainers(numContainers)
    numContainersAdded = 0
    start = time.time()
    k = []
    try:
        for container in randomContainers:
            ship.addContainer(container)
            numContainersAdded += 1
            # if not ship.isShipBalanced():
            #     k.append(numContainersAdded)
    except Exception as e:
        print('Unable to load all containers. The following exception was thrown:')
        print(e)

    finally:
        end = time.time()
        print(numContainersAdded, 'added to ship')
        print(f'Script took {end - start:0f} seconds')
        print(
            f"Number of crane operations using a single crane was: {ship.getNumberOfOperationsInShip()}")
    
    print(len(ship.getAllSections()))
    print(ship.getTotalWeight())
    print(ship.getTotalWeightPort())
    print(ship.getTotalWeightStarboard())
    print(ship.isShipBalanced())
    print()
    # print(k)

    ship.saveToFile()
    ship.readFromFile()
    ship.saveToFile("shipSave2")




if __name__ == '__main__':
    main()
