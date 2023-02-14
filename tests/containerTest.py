import sys
import os
import random
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from container import Container, createRandomContainer, createRandomContainers

def main():
    # Single container test
    # ---------------------
    c1 = Container(20, "ID1", 5)
    assert c1.getId() == "ID1", \
        f"Container id  should be ID1 but was {c1.getId()}"
    assert c1.getCapacity() == 20, \
        f"Container capacity should be 20 but was {c1.getCapacity()}"
    assert c1.getLoad() == 5, \
        f"Container load should be 5 but was {c1.getLoad()}"
    assert c1.getTotalWeight() == 7, \
        f"Total container weight weight should be 7 but was {c1.getTotalWeight()}"
    assert c1.getWeight() == 2, \
        f"Container inherit weight should be 2 but was {c1.getWeight()}"

    c1.setLoad(20)
    assert c1.getLoad() == 20, \
        f"Container load should be 20 but was {c1.getLoad()}"
    assert c1.getTotalWeight() == 22, \
        f"Total container weight weight should be 22 but was {c1.getTotalWeight()}"

    c2 = Container(40, "ID2", 7)
    assert c2.getId() == "ID2", \
        f"Container id  should be ID2 but was {c2.getId()}"
    assert c2.getCapacity() ==  22, \
        f"Container capacity should be 22 but was {c2.getCapacity()}"
    assert c2.getLoad() == 7, \
        f"Container load should be 7 but was {c2.getLoad()}"
    assert c2.getTotalWeight() == 11, \
        f"Total container weight weight should be 11 but was {c2.getTotalWeight()}"
    assert c2.getWeight() == 4, \
        f"Container inherit weight should be 4 but was {c2.getWeight()}"

    # Random container test
    # ---------------------
    random.seed(1)
    rc1 = createRandomContainer()
    assert isinstance(rc1, Container), \
        f"The object should be a container but was {type(c1).__name__}"
    rc1.setLoad(10)
    assert rc1.getLoad() == 10, \
        f"Container load should be 7 but was {rc1.getLoad()}"
    
    randomContainers = createRandomContainers(5)
    assert len(randomContainers)==5, \
        f"The number of containers should be 5 but was {len(randomContainers)}"
    for container in randomContainers:
        assert isinstance(container, Container), \
            f"The object should be a container but was {type(container).__name__}"

    print("container.py tests passed")

if __name__ == '__main__':
    main()
