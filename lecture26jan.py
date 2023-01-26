# TPK 4186 - 2023 - Assignment

# Teacher philospy: Few to none comments in code. The program should be self explaining.
# Dont use packages. e.g. pandas.

# There is no need for exeption handeling. The program is a contract between the
# creater and user. It can for example come with instructions which is the
# contract.

# There is no preference in using OOP. As the program written here is basicly OOP.

# It is possible to submit multiple times. Every time you will get comments on
# how to perform better.

# 1. Imported modules
# -------------------

import sys

# 2. Containers
# -------------------

def Container_New(serialNumber, length, weight, cargo):
    return [serialNumber, length, weight, cargo]

def Container_NewSmall(serialNumber, cargo):
    return Container_New(serialNumber, 20, 2, cargo)

def Container_NewBig(serialNumber, cargo):
    return Container_New(serialNumber, 40, 4, cargo)

def Container_GetSerialNumber(container):
    return container[0]

def Container_SetSerialNumber(container, serialNumber):
    container[0] = serialNumber

def Container_GetLength(container):
    return container[1]

def Container_SetLength(container, length):
    container[1] = length

def Container_GetWeight(container):
    return container[2]

def Container_SetWeight(container, weight):
    container[2] = weight

def Container_GetCargo(container):
    return container[3]

def Container_SetCargo(container, cargo):
    # Require: 0 <= cargo <= 40
    container[3] = cargo

def Container_GetTotalWeight(container):
    return Container_GetWeight(container) + Container_GetCargo(container)

# 3.Ships
# -------

def Ship_New(length, width, height):
    return [length, width, height, []]

def Ship_GetLength(ship):
    return ship[0]

def Ship_SetLength(ship, length):
    ship[0] = length

def Ship_GetWidth(ship):
    return ship[1]

def Ship_SetWidth(ship, width):
    ship[1] = width

def Ship_GetHeight(ship):
    return ship[2]

def Ship_SetHeight(ship, height):
    ship[2] = height

def Ship_GetContainers(ship):
    return ship[3]

def Ship_GetNumberOfContainers(ship):
    return len(ship[3])

def Ship_getNthContainer(ship, index):
    containers = Ship_GetContainers(ship)
    return containers[index]

def Ship_InsertContainer(ship, container, index):
    containers = Ship_GetContainers(ship)
    containers.insert(index, container)

def Ship_AppendContainer(ship, container):
    containers = Ship_GetContainers(ship)
    containers.append(container)

def Ship_PushContainer(ship, container):
    containers = Ship_GetContainers(ship)
    containers.push(container)

def Ship_PopContainer(ship):
    containers = Ship_GetContainers(ship)
    return containers.pop()

def Ship_LoadContainer(ship, newContainer):
    newContainerWeight = Container_GetWeight(newContainer)
    loaded = False
    i = 0
    while i<Ship_GetNumberOfContainers(ship):
        container = Ship_getNthContainer(ship, i)
        containerWeight = Container_GetWeight(container)
        if containerWeight <= newContainerWeight:
            Ship_InsertContainer(ship, newContainer, i)
            loaded = True
            break
        i = i + 1
    if not loaded:
        Ship_AppendContainer(ship, newContainer)


# 4. Printer
# ----------

def Printer_PrinterContainer(container):
    serialNumber = Container_GetSerialNumber(container)
    length = Container_GetLength(container)
    weight = Container_GetWeight(container)
    cargo = Container_GetCargo(container)
    totaltWeight = Container_GetTotalWeight(container)
    print(str(serialNumber) + " " + str(length) + " " + str(weight) + " " + str(cargo) + " " + str(totaltWeight))

def Printer_PrintShip(ship):
    length = Ship_GetLength(ship)
    width = Ship_GetWidth(ship)
    height = Ship_GetHeight(ship)
    containers = Ship_GetContainers(ship)
    print("Ship:")
    print("L: "+ str(length) + " W: " + str(width) + " H: " + str(height))
    print("Containers:")
    for container in containers:
        Printer_PrinterContainer(container)
    print()

# X. Main
# -------

ship = Ship_New(23, 22, 18)
c1 = Container_NewSmall(10001, 10)
c2 = Container_NewBig(10002, 15)
c3 = Container_NewSmall(10003, 15)
c4 = Container_NewBig(10004, 20)
c5 = Container_NewBig(10005, 15)

Ship_LoadContainer(ship, c1)
Ship_LoadContainer(ship, c2)
Ship_LoadContainer(ship, c3)
Ship_LoadContainer(ship, c4)
Ship_LoadContainer(ship, c5)

# Container_SetSerialNumber(c1, 2000)
# Container_SetLength(c1, 40)
# Container_SetWeight(c1, 4)
# Container_SetCargo(c1, 17)

Printer_PrintShip(ship)
#Printer_PrinterContainer(c3)

