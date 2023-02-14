from container import Container
from container import createRandomContainers
from shipSection import ShipSection
from containerStack import ContainerStack

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
    
    def getSection(self, sectionId: int) -> List[ShipSection]:
        for section in self.freeSections:
            if section.getSectionId() == sectionId:
                return section
        for section in self.fullSections:
            if section.getSectionId() == sectionId:
                return section
            
    def setSection(self, sectionId: int, newSection: ShipSection) -> None:
        for section in self.freeSections:
            if section.getSectionId() == sectionId:
                self.freeSections.remove(section)
        for section in self.fullSections:
            if section.getSectionId() == sectionId:
                self.fullSections.remove(section)
        
        if newSection.isFull():
            self.fullSections.append(newSection)
        else:
            self.freeSections.append(newSection)

    def updateShipWeight(self) -> None:  # Johan mener denne kan slettes?
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

    def countContainers(self) -> int:
        count = 0
        allSections = self.fullSections + self.freeSections
        for section in allSections:
            count += section.countContainers()
        return count

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
            if section.getSectionId() in [1, 3, 5]:
                totalWeightStarboard += section.getSectionWeight()
        return totalWeightStarboard

    def getTotalWeightPort(self) -> int:
        totalWeightPort = 0
        allSections = self.getAllSections()
        for section in allSections:
            if section.getSectionId() in [0, 2, 4]:
                totalWeightPort += section.getSectionWeight()
        return totalWeightPort

    def getTotalWeightSections(self) -> List[int]:
        sectionWeights = [0, 0, 0]
        allSections = self.getAllSections()
        for section in allSections:
            sectionId = section.getSectionId()
            if sectionId in [0, 1]:
                sectionWeights[0] += section.getSectionWeight()
            elif sectionId in [2, 3]:
                sectionWeights[1] += section.getSectionWeight()
            elif sectionId in [4, 5]:
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

        #print("The ship is loaded correctly")
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
                        for containers in section.getStack((w, l)).getContainers():
                            for container in containers:
                                f.write(container.getId() + "\t")
                                f.write(str(container.getSize()) + "\t")
                                f.write(str(container.getWeight()) + "\t")
                                f.write(str(container.getCapacity()) + "\t")
                                f.write(str(container.getLoad()) + "\t")
                                f.write("-\t")
                        f.write("\n")

def readFromFile(filename="shipSave", shipID = "S1") -> Ship2:
    ship = Ship2(shipID = shipID)
    section = None

    with open(os.path.join(ROOT, filename + ".tsv"), "r") as f:
        sectionId = 0
        widthCounter = 0
        lengthCounter = 0
        listFor20Containers = []
        for line in f:
            if line.startswith("Section: "):
                if section:
                    #print(section.getSectionWeight())
                    ship.setSection(sectionId, section)
                    #print(ship.getSection(sectionId).getSectionWeight())
                sectionId = int(line[9])
                section = ShipSection(sectionId, int(ship.defaultDimensions['W']/2), int(ship.defaultDimensions['L']/6), int(ship.defaultDimensions['H']))
                width = section.getWidth()
                lengthCounter = 0
                continue
            stack = ContainerStack(sectionId, (widthCounter, lengthCounter), ship.defaultDimensions['H'])
            rowInfo = line.split("-")
            for info in rowInfo:
                infoSplitted = info.strip("\n").strip("\t").split("\t")
                if(len(infoSplitted)==1):
                    continue
                container = Container(int(infoSplitted[1]), infoSplitted[0], int(infoSplitted[4]))
                if container.getSize()==40:
                    stack.addContainer([container])
                elif container.getSize()==20 and listFor20Containers:
                    listFor20Containers.append(container)
                    stack.addContainer(listFor20Containers)
                    listFor20Containers = []
                else:
                    listFor20Containers.append(container)
            section.setStack((widthCounter, lengthCounter), stack)
            widthCounter+=1
            if widthCounter == width:
                widthCounter=0
                lengthCounter+=1
    ship.setSection(sectionId, section)
    return ship

def main():
    ship = Ship2()
    numContainers = 20000
    start = time.time()

    randomContainers = createRandomContainers(numContainers)
    print('Tid = ', time.time() - start)
    numContainersAdded = 0
    start = time.time()
    k = []
    try:
        for container in randomContainers:
            ship.addContainer(container)
            numContainersAdded += 1
            if not ship.isShipBalanced():
                k.append(numContainersAdded)
    except Exception as e:
        print('Unable to load all containers. The following exception was thrown:')
        print(e)

    finally:
        end = time.time()
        print(numContainersAdded, 'added to ship')
        print(f'Script took {end - start:0f} seconds')
        print(
            f"Number of crane operations using a single crane was: {ship.getNumberOfOperationsInShip()}\nAmount of minutes used loading ship: {ship.getNumberOfOperationsInShip()*4}")
    
    print(len(ship.getAllSections()))
    print("Total weight: " + str(ship.getTotalWeight()))
    print(ship.getTotalWeightPort())
    print(ship.getTotalWeightStarboard())
    print(ship.isShipBalanced())
    print()
    print(k)
    print("DSADASD")
    print(ship.countContainers())
    print(randomContainers[ship.countContainers()+1].getSize())

    ship.saveToFile()

    ship2 = readFromFile()
    print("Total weight: " + str(ship2.getTotalWeight()))
    ship2.saveToFile("shipSave2")
    # ship.readFromFile()
    # ship.saveToFile("shipSave2")

    # add bitwise check


if __name__ == '__main__':
    main()
