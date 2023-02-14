import sys
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from container import Container
from containerStack import ContainerStack
import math
import filecmp

def testDecreasingOrder(containerStack: ContainerStack):
    containerList = containerStack.getContainers()
    prevContainerWeight = math.inf
    for i in range(len(containerStack.containers)):
        currContainerWeight = sum([container.getTotalWeight()
                                  for container in containerList[i]])
        if prevContainerWeight < currContainerWeight:
            raise Exception(
                f"containerStack at location {containerStack.getLocation()} is not in decreasing order.")
        else:
            prevContainerWeight = currContainerWeight


def main():
    # 0. Setup
    # --------
    section = 0
    loc = (0, 0)
    maxHeight = 10
    containerStack = ContainerStack(section, loc, maxHeight)

    # 1. Test weight management and number of loading/unloading operations
    # -----------------------------
    # si denotes small container i
    # bi denotes big container i
    # ti denotes two small containers in a list
    b1 = Container(40, 'b1', 5)  # weights 9
    b2 = Container(40, 'b2', 4)  # weights 8
    b3 = Container(40, 'b3', 6)  # weights 10
    c1 = Container(20, 'c1', 1)  # weights 3
    c2 = Container(20, 'c2', 2)  # weights 4
    c3 = Container(20, 'c3', 10)  # weights 12
    c4 = Container(20, 'c4', 10)  # weights 12
    t1 = [c1, c2]  # weights 7
    t2 = [c3, c4]  # weight 24

    assert containerStack.getTotalWeight() == 0, \
        f"Total container stack weight should be 0 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 0, \
        f"Total container stack weight should be 0 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 0, \
        f"Total number of operations performed on container stack should be 0 but was {containerStack.getNumOperations()}"

    containerStack.addContainer(b1)
    testDecreasingOrder(containerStack)
    assert containerStack.getTotalWeight() == 9, \
        f"Total container stack weight should be 9 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 9, \
        f"Total container stack weight should be 9 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 1, \
        f"Total number of operations performed on container stack should be 1 but was {containerStack.getNumOperations()}"

    containerStack.addContainer(b2)
    testDecreasingOrder(containerStack)
    assert containerStack.getTotalWeight() == 17, \
        f"Total container stack weight should be 17 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 8, \
        f"Total container stack weight should be 8 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 2, \
        f"Total number of operations performed on container stack should be 2 but was {containerStack.getNumOperations()}"

    containerStack.addContainer(b3)
    testDecreasingOrder(containerStack)
    assert containerStack.getTotalWeight() == 27, \
        f"Total container stack weight should be 27 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 8, \
        f"Total container stack weight should be 8 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 7, \
        f"Total number of operations performed on container stack should be 7 but was {containerStack.getNumOperations()}"

    containerStack.addContainer(t1)
    testDecreasingOrder(containerStack)
    assert containerStack.getTotalWeight() == 34, \
        f"Total container stack weight should be 34 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 7, \
        f"Total container stack weight should be 7 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 9, \
        f"Total number of operations performed on container stack should be 9 but was {containerStack.getNumOperations()}"

    containerStack.addContainer(t2)
    testDecreasingOrder(containerStack)
    assert containerStack.getTotalWeight() == 58, \
        f"Total container stack weight should be 58 but was {containerStack.getTotalWeight()}"
    assert containerStack.getTopWeight() == 7, \
        f"Total container stack weight should be 7 but was {containerStack.getTopWeight()}"
    assert containerStack.getNumOperations() == 21, \
        f"Total number of operations performed on container stack should be 21 but was {containerStack.getNumOperations()}"
    
    containerStack.saveToFile("containerStackTestTemp")
    assert filecmp.cmp('containerStackTestTemp.tsv', 'containerStackTestOriginal.tsv'), \
        f"The file created should have identical content to the original save file"
    os.remove("containerStackTestTemp.tsv")
    
    print('containerStackTest.py tests passed')

if __name__ == '__main__':
    main()
