from containerStack import ContainerStack
from container import Container
import unittest

def main():
    print('-'*10, 'Testing containerStack', '-'*10)

    # Setup
    section = 0
    loc = (0,0)
    maxHeight = 10

    # 1. Test weight management
    # -----------------------------
    #si denotes small container i
    #bi denotes big container i
    c1 = Container(20,'1',1)
    c2 = Container(20,'2', 2)
    b1 = Container(40, '3', 4)
    b2 = Container(40, '4', 5)
    b3 = Container(40, '5', 6)
    containers = [c1, c2, b1, b2, b3]
    totalWeight = [container.getTotalWeight() for container in containers]
    b3_weight = b3.getTotalWeight()

    containerStack = ContainerStack(section, loc, maxHeight)







    # 1. Test ship weight functions
    # -----------------------------







    # 1. Test ship weight functions
    # -----------------------------






    # 1. Test ship weight functions
    # -----------------------------