"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.3. Charge permanente.


____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### IMPORTS ###
from dataclasses import dataclass


### DB MANAGEMENT ###


### CODE ###
class DeadLoads:
    """4.1.4. Charge permanente.

    Args:
        weight (list, optional): poids de tous les matériaux de construction incorporés au bâtiment
        et destinés à être supportés de façon permanente par l'élément.
        partitions (bool, optional): Poids des cloisons. Defaults to False.
    """

    def __init__(self, *material, add_partitions=False):
        self.material = material
        self.partitions = add_partitions

    def calculate(self):
        dead_loads = 0
        if self.partitions:
            dead_loads += 1
        for d in self.material:
            dead_loads += d

        return dead_loads


### TESTS ###
def tests():
    """tests pour la classe DeadLoads"""
    print("")

    test = DeadLoads(1, 2, 3, True).calculate()
    expected_result = 7
    if test != expected_result:
        print("test -> FAILED")
        print(f"result = {test}")
        print(f"expected = {expected_result}\n")
    else:
        print("test -> PASSED\n")


### RUN FILE ###
if __name__ == "__main__":
    print("\n------START_TESTS------")
    tests()
    print("-------END_TESTS-------\n")
    # pass

### END ###
