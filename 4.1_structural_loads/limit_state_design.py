"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.2. Charges spécifiées et leurs effets.
    D -> Charge permanente | charge constante exercée par le poids des composants du bâtiment;
    L -> Surcharge | charge variable due à l'usage prévu (y compris les charges dues aux ponts
         roulants et à la pression des liquides dans les récipients);   
    S -> Charge variable due à la neige, y compris la glace et la charge correspondante de pluie;
    W -> Charge due au vent | charge variable due au vent;
    E -> charge et effets dus aux séismes | charge peu fréquente causée par les séismes.
    
4.1.3. Calcul aux états limites.
    Effectue le calcul pour ELU et ELTS en fonction des charges spécifiées et des conditions
    d'application des charges.
____________________________________________________________________________________________________

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

# IMPORTS
from dataclasses import dataclass
from dead_loads import DeadLoads


# CODE
@dataclass
class LimitStatesDesign:
    """4.1.2. Charges spécifiées et leurs effets.
        4.1.3. Calcul aux états limites.

    Args:
        dead: Charge permanente (D).
        live: Surcharge due à l'usage (L).
        snow: Charge due à la neige (S).
        wind: Charge due au vent (W).
        earthquake: Charge et effets dus aux séismes (E).
        counter_d: Charge permanente pondérée contraire.
        liquid_l: Liquide contenu dans des réservoirs.
        storage_area: Aire de stockage, aire réservé à l'équipement ou local technique.
        exterior_area: Toit ou aire extérieur.
        car_access: Aire accessible aux véhicules.
        h_s: Profondeur du sol, en m, supporté par la structure.
    """

    dead: DeadLoads = 0
    live: float = 0
    snow: float = 0
    wind: float = 0
    earthquake: float = 0
    counter_d: bool = False
    liquid_l: bool = False
    storage_area: bool = False
    exterior_area: bool = False
    car_access: bool = False
    h_s: float = 0

    def _uls_factors(self):
        d1 = 1.4
        d234 = 1.25
        l2 = 1.5
        l3 = 1
        l4 = 0.5
        l5 = 0.5
        s2 = 1
        s4 = 0.5
        s5 = 0.25

        if self.h_s > 0:
            d1 = 1.5  # 4.1.3.2. 9)
            d234 = 1.5  # 4.1.3.2. 8)
            if self.h_s > 1.2:
                d234 = max(1 + 0.6 / self.h_s, 1.25)

        if self.counter_d:
            d234 = 0.9  # 4.1.3.2. 5)

        if self.liquid_l:
            l2 = 1.25  # 4.1.3.2. 6)

        if self.storage_area:
            l3 += 0.5  # 4.1.3.2. 7)
            l4 += 0.5
            l5 += 0.5

        if self.exterior_area:
            if not self.car_access:
                s2 = 0  # 4.1.5.5. 2)
                l3 = 0
                if l5 * self.live < s5 * self.snow:
                    l5 = 0  # 4.1.5.5. 3)
                else:
                    s5 = 0
            else:
                s2 = 0.2  # 4.1.5.5. 4)
                s4 = 0.2
                s5 = 0.2

        return d1, d234, l2, l3, l4, l5, s2, s4, s5

    def _sls_factors(self):
        sls_l = 0.35

        if self.storage_area:
            sls_l = 0.5

        return sls_l

    def uls(self):
        """4.1.3.2. Résistance et stabilité.
            Tableau 4.1.3.2.-A

        Returns:
            État limite ultime
        """
        (
            d1_factor,
            d234_factor,
            l2_factor,
            l3_factor,
            l4_factor,
            l5_factor,
            s2_factor,
            s4_factor,
            s5_factor,
        ) = self._uls_factors()

        case_1 = d1_factor * self.dead
        case_2 = (
            d234_factor * self.dead
            + l2_factor * self.live
            + max(s2_factor * self.snow, 0.4 * self.wind)
        )
        case_3 = (
            d234_factor * self.dead
            + 1.5 * self.snow
            + max(l3_factor * self.live, 0.4 * self.wind)
        )
        case_4 = (
            d234_factor * self.dead
            + 1.4 * self.wind
            + max(l4_factor * self.live, s4_factor * self.snow)
        )
        case_5 = (
            self.dead + self.earthquake + l5_factor * self.live + s5_factor * self.snow
        )

        ultimate_limit_state = max(case_1, case_2, case_3, case_4, case_5)

        return ultimate_limit_state

    def sls(self):
        """4.1.3.4. Tenue en service.
            Tableau 4.1.3.4.

        Returns:
            État limite de tenue en service
        """

        case_1 = self.dead + self.live + max(0.3 * self.wind, 0.35 * self.snow)
        case_2 = (
            self.dead
            + self.wind
            + max(self._sls_factors() * self.live, 0.35 * self.snow)
        )
        case_3 = (
            self.dead
            + self.snow
            + max(0.3 * self.wind, self._sls_factors() * self.live)
        )

        serviceability_limit_state = max(case_1, case_2, case_3)

        return serviceability_limit_state


# TESTS
def uls_tests():
    """tests pour la fonction uls"""
    print("----ELU----")

    uls_default_test = LimitStatesDesign().uls()
    expected_result = 0
    if uls_default_test != expected_result:
        print("uls_default_test -> FAILED")
        print(f"result = {uls_default_test}")
        print(f"expected = {expected_result}")
    else:
        print("uls_default_test -> PASSED")

    uls_storage_test = LimitStatesDesign(
        dead=0.5,
        live=4.8,
        snow=2.5,
        wind=1,
        earthquake=1,
        counter_d=True,
        liquid_l=True,
        exterior_area=True,
        storage_area=True,
        car_access=True,
        h_s=1,
    ).uls()
    expected_result = 11.399999999999999
    if uls_storage_test != expected_result:
        print("uls_storage_test -> FAILED")
        print(f"result = {uls_storage_test}")
        print(f"expected = {expected_result}")
    else:
        print("uls_storage_test -> PASSED")


def sls_tests():
    """tests pour la fonction sls"""
    print("----ELTS----")

    sls_default_test = LimitStatesDesign().sls()
    expected_result = 0
    if sls_default_test != expected_result:
        print("sls_default_test -> FAILED")
        print(f"result = {sls_default_test}")
        print(f"expected = {expected_result}")
    else:
        print("sls_default_test -> PASSED")

    sls_storage_test = LimitStatesDesign(
        dead=2,
        live=2,
        snow=2,
        wind=2,
        earthquake=2,
        storage_area=True,
    ).sls()
    expected_result = 5
    if sls_storage_test != expected_result:
        print("sls_storage_test -> FAILED")
        print(f"result = {sls_storage_test}")
        print(f"expected = {expected_result}")
    else:
        print("sls_storage_test -> PASSED")


# RUN FILE
if __name__ == "__main__":
    print("------START_TESTS------")
    uls_tests()
    sls_tests()
    print("-------END_TESTS-------")

# END
