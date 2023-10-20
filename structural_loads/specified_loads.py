"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.2. Charges spécifiées et leurs effets.

Permet de spécifier les charges selon les catégories suivantes:
    D -> Charge permanente | charge constante exercée par le poids des composants du bâtiment;
    L -> Surcharge | charge variable due à l'usage prévu (y compris les charges dues aux ponts
         roulants et à la pression des liquides dans les récipients);   
    S -> Charge variable due à la neige, y compris la glace et la charge correspondante de pluie;
    W -> Charge due au vent | charge variable due au vent;
    E -> charge et effets dus aux séismes | charge peu fréquente causée par les séismes;
____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### IMPORTS ###
from dataclasses import dataclass


### CODE ###
@dataclass
class SpecifiedLoads:
    """4.1.2. Charges spécifiées.

    Args:
        dead (optional): Charge permanente (D). Defaults to 0.
        live (optional): Surcharge due à l'usage (L). Defaults to 0.
        snow (optional): Charge due à la neige (S). Defaults to 0.
        wind (optional): Charge due au vent (W). Defaults to 0.
        earthquake (optional): Charge et effets dus aux séismes (E). Defaults to 0.
    """

    dead: int | float = 0
    live: int | float = 0
    snow: int | float = 0
    wind: int | float = 0
    earthquake: int | float = 0


### TESTS ###
def tests():
    """tests pour la classe SpecifiedLoads"""
    print("")

    test = SpecifiedLoads(dead=0.54)
    expected_result = 0.54
    if test.dead != expected_result:
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

### END ###
