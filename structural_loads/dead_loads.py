"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.3. Charge permanente.

Permet de ...
____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### IMPORTS ###
from dataclasses import dataclass


### CODE ###
@dataclass
class DeadLoads:
    """4.1.4. Charge permanente.

    Args:
        partitions (optional): Poids des cloisons. Defaults to False.
    """

    partitions: bool = False


### TESTS ###
def tests():
    """tests pour la classe DeadLoads"""
    print("")

    test = DeadLoads()
    expected_result = False
    if test.partitions != expected_result:
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
