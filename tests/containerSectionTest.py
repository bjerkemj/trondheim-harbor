import sys
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from shipSection import ShipSection
from containerStack import ContainerStack
from container import Container

def main():
    # Setup
    # -----
    shipSection = ShipSection(1, 2, 2, 2)
    c1 = Container(40, "c1", 20)
    c2 = Container(40, "c2", 20)
    c3 = Container(40, "c3", 16)
    c4 = Container(40, "c4", 16)
    c5 = Container(40, "c5", 14)
    c6 = Container(40, "c6", 14)
    c7 = Container(40, "c7", 10)
    c8 = Container(40, "c8", 10)
    containers = [c3, c4, c5, c6, c7, c8]
    

    # Testing shipsection
    # -------------------
    assert shipSection.getSectionId() == 1, \
        f"ShipSection ID should be 1 but was {shipSection.getSectionId()}"
    assert shipSection.getWidth() == 2, \
        f"ShipSection width should be 2 but was {shipSection.getWidth()}"
    assert shipSection.getLength() == 2, \
        f"ShipSection width should be 2 but was {shipSection.getLength()}"
    assert shipSection.getMaxStackHeight() == 2, \
        f"ShipSection width should be 2 but was {shipSection.getMaxStackHeight()}"
    assert shipSection.isFull() == False, \
        f"ShipSection should not be full after initated"

    lowestWeightContainerStack = shipSection.getLowestWeightContainerStack()
    assert isinstance(lowestWeightContainerStack, ContainerStack), \
        f"getLowestWeightContainerStack() should return a ContainerStack"
    assert lowestWeightContainerStack.getTotalWeight() == 0, \
        f"The lowest weight ContainerStack should be after initiating ShipSection"
   
    shipSection.addContainerToSection(c1)
    assert shipSection.getSectionWeight() == 24, \
        f"Total weight of ShipSection should be 24 but was {shipSection.getSectionWeight()}"
    shipSection.addContainerToSection(c2)
    assert shipSection.getSectionWeight() == 48, \
        f"Total weight of ShipSection should be 48 but was {shipSection.getSectionWeight()}"
    assert shipSection.getNumOperationsInSection() == 2, \
        f"Total number of operations should be 2 but was {shipSection.getNumOperationsInSection()}"
    assert shipSection.countContainers() == 2, \
        f"Total number of operations should be 2 but was {shipSection.countContainers()}"
    
    for container in containers:
        shipSection.addContainerToSection(container)
    assert shipSection.getSectionWeight() == 152, \
        f"Total weight of ShipSection should be 152 but was {shipSection.getSectionWeight()}"
    assert shipSection.getNumOperationsInSection() == 8, \
        f"Total number of operations should be 8 but was {shipSection.getNumOperationsInSection()}"
    assert shipSection.countContainers() == 8, \
        f"Total number of operations should be 8 but was {shipSection.countContainers()}"
    
    assert shipSection.isFull() == True, \
        f"ShipSection should be full"
    
    print('shipSection.py tests passed')

if __name__ == '__main__':
    main()
