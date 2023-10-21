"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.3. Calcul aux états limites.

Effectue le calcul pour ELU et ELTS en fonction des charges spécifiées et des conditions
d'application des charges.
____________________________________________________________________________________________________

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### LOCAL IMPORTS ###
from specified_loads import SpecifiedLoads


### CODE ###
class LimitStatesDesign:
    """4.1.3. Calcul aux états limites."""

    def __init__(self, loads=SpecifiedLoads, storage_area=False):
        """4.1.3. Calcul aux états limites.

        Args:
            loads (optional): Defaults to SpecifiedLoads.
            storage_area (optional): Aires de stockage. Defaults to False.
        """
        self.dead = loads.dead
        self.live = loads.live
        self.snow = loads.snow
        self.wind = loads.wind
        self.earthquake = loads.earthquake
        self.storage_area = storage_area

    def uls(
        self,
        h_s=0,
        counter_d=False,
        liquid_l=False,
        exterior_area=False,
        car_access=False,
    ):
        """4.1.3.2. Résistance et stabilité.

        Args:
            h_s (optional): Profondeur du sol, en m, supporté par la structure. Defaults to 0.
            counter_d (optional): Charge permanente pondérée contraire. Defaults to False.
            liquid_l (optional): Liquides contenus dans des réservoirs. Defaults to False.
            exterior_area (optional): Toits ou aires extérieures. Defaults to False.
            car_access (optional): Accessible aux véhicules. Defaults to False.

        Returns:
            float: État limite ultime
        """

        dead1_factor = 1.4
        dead234_factor = 1.25
        live2_factor = 1.5
        live3_factor = 1
        live4_factor = 0.5
        live5_factor = 0.5
        snow2_factor = 1
        snow4_factor = 0.5
        snow5_factor = 0.25

        if h_s > 0:
            dead1_factor = 1.5  # 4.1.3.2. 9)
            dead234_factor = 1.5  # 4.1.3.2. 8)
            if h_s > 1.2:
                dead234_factor = max(1 + 0.6 / h_s, 1.25)

        if counter_d:
            dead234_factor = 0.9  # 4.1.3.2. 5)

        if liquid_l:
            live2_factor = 1.25  # 4.1.3.2. 6)

        if self.storage_area:
            live3_factor += 0.5  # 4.1.3.2. 7)
            live4_factor += 0.5
            live5_factor += 0.5

        if exterior_area:
            if not car_access:
                snow2_factor = 0  # 4.1.5.5. 2)
                live3_factor = 0
                if live5_factor * self.live < snow5_factor * self.snow:
                    live5_factor = 0  # 4.1.5.5. 3)
                else:
                    snow5_factor = 0
            else:
                snow2_factor = 0.2  # 4.1.5.5. 4)
                snow4_factor = 0.2
                snow5_factor = 0.2

        # Combinaisons de charges (Tableau 4.1.3.2.-A)
        case_1 = dead1_factor * self.dead
        case_2 = (
            dead234_factor * self.dead
            + live2_factor * self.live
            + max(snow2_factor * self.snow, 0.4 * self.wind)
        )
        case_3 = (
            dead234_factor * self.dead
            + 1.5 * self.snow
            + max(live3_factor * self.live, 0.4 * self.wind)
        )
        case_4 = (
            dead234_factor * self.dead
            + 1.4 * self.wind
            + max(live4_factor * self.live, snow4_factor * self.snow)
        )
        case_5 = (
            self.dead
            + self.earthquake
            + live5_factor * self.live
            + snow5_factor * self.snow
        )

        ultimate_limit_state = max(case_1, case_2, case_3, case_4, case_5)
        return ultimate_limit_state

    def sls(self):
        """4.1.3.4. Tenue en service.

        Returns:
            float: État limite de tenue en service
        """

        live_factor = 0.35
        if self.storage_area:
            live_factor = 0.5

        # Combinaisons de charges (Tableau 4.1.3.4.)
        case_1 = self.dead + self.live + max(0.3 * self.wind, 0.35 * self.snow)
        case_2 = self.dead + self.wind + max(live_factor * self.live, 0.35 * self.snow)
        case_3 = self.dead + self.snow + max(0.3 * self.wind, live_factor * self.live)

        serviceability_limit_state = max(case_1, case_2, case_3)
        return serviceability_limit_state


### TESTS ###
def uls_tests():
    """tests pour la fonction uls"""
    print("\n----ELU----\n")

    uls_default_test = LimitStatesDesign().uls()
    expected_result = 0
    if uls_default_test != expected_result:
        print("uls_default_test -> FAILED")
        print(f"result = {uls_default_test}")
        print(f"expected = {expected_result}\n")
    else:
        print("uls_default_test -> PASSED\n")

    uls_storage_test = LimitStatesDesign(
        SpecifiedLoads(dead=0.5, live=4.8, snow=2.5, wind=1, earthquake=1),
        storage_area=True,
    ).uls(h_s=1, counter_d=True, liquid_l=True, exterior_area=True, car_access=True)
    expected_result = 11.399999999999999
    if uls_storage_test != expected_result:
        print("uls_storage_test -> FAILED")
        print(f"result = {uls_storage_test}")
        print(f"expected = {expected_result}\n")
    else:
        print("uls_storage_test -> PASSED\n")


def sls_tests():
    """tests pour la fonction sls"""
    print("\n----ELTS----\n")

    sls_default_test = LimitStatesDesign().sls()
    expected_result = 0
    if sls_default_test != expected_result:
        print("sls_default_test -> FAILED")
        print(f"result = {sls_default_test}")
        print(f"expected = {expected_result}\n")
    else:
        print("sls_default_test -> PASSED\n")

    sls_storage_test = LimitStatesDesign(
        SpecifiedLoads(dead=2, live=2, snow=2, wind=2, earthquake=2),
        storage_area=True,
    ).sls()
    expected_result = 5
    if sls_storage_test != expected_result:
        print("sls_storage_test -> FAILED")
        print(f"result = {sls_storage_test}")
        print(f"expected = {expected_result}\n")
    else:
        print("sls_storage_test -> PASSED\n")


### RUN FILE ###
if __name__ == "__main__":
    # print("\n------START_TESTS------")
    # uls_tests()
    # sls_tests()
    # print("-------END_TESTS-------\n")
    pass

### END ###
