from ship import Ship
from container import Container
import pprint


def main():
    # 1. Test ship weight functions
    # -----------------------------
    dim = {'L': 3, 'W': 4, 'H': 3}
    ship = Ship(dim, '3by3ship')
    containers = ship.boxes

    c1 = Container(20, "c1", 10)
    c2 = Container(20, "c10", 10)
    c3 = Container(20, "c10", 10)
    c4 = Container(20, "c10", 10)
    c5 = Container(20, "c10", 10)
    c6 = Container(20, "c10", 10)
    c7 = Container(20, "c10", 10)


    containers[0][0][0] = c1
    containers[0][0][1] = c2
    containers[0][1][1] = c3
    containers[0][1][2] = c4
    containers[0][2][2] = c5
    containers[0][2][3] = c6
    
    ship.saveToFile()
    print("pølse")
    ship.readFromFile()
    ship.saveToFile("standardSave2")
    print()

    print(12+12+12+12+12+12)
    print(ship.getTotalWeight())
    print()

    print("Port")
    print(12+12+12)
    print(ship.getTotalWeightPort())
    print()

    print("Starboard")
    print(12+12+12)
    print(ship.getTotalWeightStarboard())
    print()

    weights = ship.getTotalWeightSections()
    print("Sections")
    print(weights[0])
    print(weights[1])
    print(weights[2])
    print()

    ship.isShipBalanced()


if __name__ == '__main__':
    main()