from container import Container, createRandomContainers
from shipSection import ShipSection
from containerStack import ContainerStack

import numpy as np
import random
import os
import filecmp
import time

ROOT = os.path.dirname(os.path.abspath(__file__))


class Ship:
    defaultDimensions = {"L": 24, "W": 22, "H": 18}

    def __init__(self, dimensions: dict = defaultDimensions, shipID: str = None):
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

    def getShipID(self):
        return self.shipID

    def isFull(self) -> bool:
        return len(self.freeSections) == 0

    def getAllSections(self) -> 'list[ShipSection]':
        return self.freeSections + self.fullSections

    def getSection(self, sectionId: int) -> 'list[ShipSection]':
        for section in self.getAllSections():
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

    def addContainers(self, containers: 'list[Container]'):
        for container in containers:
            self.addContainer(container)

    def lookForContainer(self, id: str) -> bool:
        for section in self.getAllSections():
            if section.lookForContainer(id):
                return True
        return False

    def addContainersFourCranes(self, containers: 'list[Container]') -> None:
        craneActivity = [[], [], [], []]
        info = None
        crane = None

        for container in containers:
            if self.isFull():
                print('Ship is full, no more containers may be added')
                return craneActivity

            lowestWeightSection = self.getLowestWeightShipSection()
            section = lowestWeightSection.getSectionId()
            if container.size == 20:
                if self.holdingSpot:
                    containers = [self.holdingSpot.pop(), container]
                    info = lowestWeightSection.addContainerToSectionFourCranes(
                        containers)
                else:
                    self.holdingSpot.append(container)
            else:
                info = lowestWeightSection.addContainerToSectionFourCranes(
                    container)
            if lowestWeightSection.isFull():
                self.freeSections.remove(lowestWeightSection)
                self.fullSections.append(lowestWeightSection)
            if info:
                lengthPos = info[0][1]
                operations = info[1]
                if section == 2 or section == 4 or section == 6:
                    info[0] = (info[0][0]+11, lengthPos)
                if section == 1 or section == 2:
                    if lengthPos == 3:
                        crane = 1
                    else:
                        crane = 0
                elif section == 3 or section == 4:
                    info[0] = (info[0][0], lengthPos + 4)
                    if lengthPos == 0 or lengthPos == 1:
                        crane = 1
                    else:
                        crane = 2
                else:
                    info[0] = (info[0][0], lengthPos + 8)
                    if lengthPos == 0:
                        crane = 2
                    else:
                        crane = 3
                for i in range(operations):
                    craneActivity[crane].append(info[0])
                info = None
                crane = None
        return craneActivity

    def removeContainer(self, id: str) -> 'list[Container]':
        if not self.lookForContainer(id):
            return None
        for section in self.getAllSections():
            if section.lookForContainer(id):
                return section.removeContainer(id)

    def emptyShip(self) -> 'list[Container]':
        containers = []
        for section in self.getAllSections():
            containers += section.emptySection()
        return containers

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

    def getAllSections(self) -> 'list[ShipSection]':
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

    def getTotalWeightSections(self) -> 'list[int]':
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

    def isShipBalanced(self, x_perc=0.05, y_perc=0.1, printOutput: bool = False) -> bool:
        weightPortside = self.getTotalWeightPort()
        weightStarboard = self.getTotalWeightStarboard()
        weightSection = self.getTotalWeightSections()

        if weightPortside > weightStarboard * (1 + x_perc):
            if printOutput:
                print("Port side to heavy")
            return False

        if weightPortside < weightStarboard * (1 - x_perc):
            if printOutput:
                print("Starboard to heavy")
            return False

        if weightSection[1] > weightSection[0] * (1 + y_perc) or weightSection[2] > weightSection[0] * (1 + y_perc):
            if printOutput:
                print("Mid or stern section to heavy")
            return False

        if weightSection[0] > weightSection[1] * (1 + y_perc) or weightSection[2] > weightSection[1] * (1 + y_perc):
            if printOutput:
                print("Bow or stern section to heavy")
            return False

        if weightSection[0] > weightSection[2] * (1 + y_perc) or weightSection[1] > weightSection[2] * (1 + y_perc):
            if printOutput:
                print("Bow or mid section to heavy")
            return False
        if printOutput:
            print("The ship is loaded correctly")
        return True

    def saveToFile(self, filename: str = "shipSave") -> None:
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


def readFromFile(filename: str = "shipSave", shipID: str = None) -> Ship:
    ship = Ship(shipID=shipID)
    section = None

    with open(os.path.join(ROOT, filename + ".tsv"), "r") as f:
        sectionId = 0
        widthCounter = 0
        lengthCounter = 0
        listFor20Containers = []
        for line in f:
            if line.startswith("Section: "):
                if section:
                    # print(section.getSectionWeight())
                    ship.setSection(sectionId, section)
                    # print(ship.getSection(sectionId).getSectionWeight())
                sectionId = int(line[9])
                section = ShipSection(sectionId, int(ship.defaultDimensions['W']/2), int(
                    ship.defaultDimensions['L']/6), int(ship.defaultDimensions['H']))
                width = section.getWidth()
                lengthCounter = 0
                continue
            stack = ContainerStack(
                sectionId, (widthCounter, lengthCounter), ship.defaultDimensions['H'])
            rowInfo = line.split("-")
            for info in rowInfo:
                infoSplitted = info.strip("\n").strip("\t").split("\t")
                if(len(infoSplitted) == 1):
                    continue
                container = Container(
                    int(infoSplitted[1]), infoSplitted[0], int(infoSplitted[4]))
                if container.getSize() == 40:
                    stack.addContainer([container])
                elif container.getSize() == 20 and listFor20Containers:
                    listFor20Containers.append(container)
                    stack.addContainer(listFor20Containers)
                    listFor20Containers = []
                else:
                    listFor20Containers.append(container)
            section.setStack((widthCounter, lengthCounter), stack)
            widthCounter += 1
            if widthCounter == width:
                widthCounter = 0
                lengthCounter += 1
    ship.setSection(sectionId, section)
    return ship


def fourCraneNumOfOps(craneActivity: 'list[list[tuple]]') -> int:
    totalOperations = max([len(ca) for ca in craneActivity])
    maxNum = max([len(ca) for ca in craneActivity])
    for i, ca in enumerate(craneActivity):
        ca = (ca + maxNum * [None])[:maxNum]
        craneActivity[i] = ca
    for i in range(maxNum):
        if (craneActivity[0][i] and craneActivity[1][i]) and (craneActivity[0][i][0] == craneActivity[1][i][0]) and (craneActivity[0][i][1]+1 == craneActivity[1][i][1]):
            totalOperations += 1
        if (craneActivity[1][i] and craneActivity[2][i]) and (craneActivity[1][i][0] == craneActivity[2][i][0]) and (craneActivity[1][i][1]+1 == craneActivity[2][i][1]):
            totalOperations += 1
        if (craneActivity[2][i] and craneActivity[3][i]) and (craneActivity[2][i][0] == craneActivity[3][i][0]) and (craneActivity[2][i][1]+1 == craneActivity[3][i][1]):
            totalOperations += 1
    return totalOperations


def main():
    random.seed(1)
    ship = Ship()
    shipFourCranes = Ship()
    numContainers = 20000
    randomContainers = createRandomContainers(numContainers)
    start = time.time()
    k = []
    try:
        for container in randomContainers:
            ship.addContainer(container)
            if not ship.isShipBalanced():
                k.append(ship.countContainers())
    except Exception as e:
        print('Unable to load all containers. The following exception was thrown:')
        print(e)

    finally:
        end = time.time()
        print(f'Script took {end - start:0f} seconds')
        print()
        print("Statistics of the shipload with one crane:")
        print(
            f"Number of crane operations using a single crane : {ship.getNumberOfOperationsInShip()}")
        print(
            f"Minutes spent loading ship: {ship.getNumberOfOperationsInShip()*4}")
        print(
            f"Minutes it would take unloading using a single crane: {ship.countContainers()*4}")
        print(f"Containers loaded: {ship.countContainers()}")
        ship.isShipBalanced(printOutput=True)
        print(f"Ship was balanced after container {k[-1]+1} was loaded.")
        print(f"Total weight of ship: " + str(ship.getTotalWeight()))

    print()
    print("Statistics of the shipload with four cranes:")
    operations = fourCraneNumOfOps(
        shipFourCranes.addContainersFourCranes(randomContainers))
    print(f"Number of crane operations using a four cranes: {operations}")
    print(f"Minutes spent loading ship: {operations*4}")
    print(f"Containers loaded: {shipFourCranes.countContainers()}")
    shipFourCranes.isShipBalanced(printOutput=True)
    print(f"Ship was balanced after container {k[-1]+1} was loaded.")
    print(f"Total weight of ship: " + str(shipFourCranes.getTotalWeight()))

    print()
    print("Save the ship to file and create a new one from the save file:")
    ship.saveToFile()
    ship2 = readFromFile()
    print(f"Original ship weight: {ship.getTotalWeight()}")
    print(f"Copy ship weight: {ship2.getTotalWeight()}")
    print(f"Original ship container count: {ship.countContainers()}")
    print(f"Copy ship cointainer count: {ship2.countContainers()}")

    ship2.saveToFile("shipSave2")
    assert filecmp.cmp('shipSave.tsv', 'shipSave2.tsv'), \
        f"The save file from the copy ship should equal the save file from the original ship"
    os.remove("shipSave2.tsv")
    print("Bitwise check of the two saves is identical, as expected.")
    print()

    print("Ship where we add 1000 empty containers, then 1000 full containers:")
    stressTestShip = Ship()
    stressTestContainers = []
    stressTestContainers += [Container(40, "FAKEID", 0)]*1000
    stressTestContainers += [Container(40, "FAKEID", 22)]*1000
    stressTestShip.addContainers(stressTestContainers)
    stressTestShip.isShipBalanced(printOutput=True)
    print(f"Ship contains: {stressTestShip.countContainers()} containers")
    print(
        f"One crane used: {stressTestShip.getNumberOfOperationsInShip()} operations")
    print(f"This number is as expected. First 1000 containers are loaded using 1000 operations. Then 1000 more containers are loaded using 1000 more operations. Since the 1000 last are heavier, they need to be placed below the inital 1000 containers. Each level in the ship is 22*12=264 containers (only loading 40ft containers). That means the heavy containers need to move 1000/264=3.787 in each stack to be place on the bottom (container need to be moved both in and out). This results in 1000 + 1000 + 3.787*1000 = 9574 which is roughly equal to 9552 operations.")


if __name__ == '__main__':
    main()
