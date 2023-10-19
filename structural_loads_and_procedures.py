"""
Script pour effectuer les calculs selon la section
4.1. Charges et methodes de calculs du CNB2020.

Auteur: GabPoulin
email: poulin33@me.com
"""
from dataclasses import dataclass


@dataclass
class LimitStatesDesign:
    """4.1.3. Calcul aux états limites."""

    dead: int | float = 0
    live: int | float = 0
    snow: int | float = 0
    wind: int | float = 0
    earthquake: int | float = 0
    storage_area: bool = False
    exterior_area: bool = False
    car_access: bool = False

    def elu(self, counter_d=False, liquid_l=False, h_s=0):
        """Calcul ELU selon CNB-2020: Tableau 4.1.3.2.-A.

        Args:
            counter_d (optional): Charge permanente pondérée contraire. Defaults to False.
            liquid_l (optional): Coeff. de surcharge réduit pour liquides. Defaults to False.
            h_s (optional): Profondeur du sol, en m, supporté par la structure. Defaults to 0.

        Returns:
            float: État Limite Ultime
        """

        d1 = 1.4
        d_ = 1.25
        l2 = 1.5
        l3 = 1
        l4 = 0.5
        l5 = 0.5
        s2 = 1
        s4 = 0.5
        s5 = 0.25

        # 4.1.3.2.
        # 6)
        if liquid_l:
            l2 = 1.25
        # 7)
        if self.storage_area:
            l3 += 0.5
            l4 += 0.5
            l5 += 0.5
        # 8) & 9)
        if h_s > 0:
            d_ = 1.5
            if h_s > 1.2:
                d_ = max(1 + 0.6 / h_s, 1.25)
            d1 = 1.5
        # 5)
        if counter_d:
            d_ = 0.9

        # 4.1.5.5.
        if self.exterior_area:
            # 3)
            if not self.car_access:
                s2 = 0
                l3 = 0
                if l5 * self.live < s5 * self.snow:
                    l5 = 0
                else:
                    s5 = 0
            # 4) a)
            s2 = 0.2
            s4 = 0.2
            s5 = 0.2

        # Combinaisons de charges (Tableau 4.1.3.2.-A)
        c_1 = d1 * self.dead
        c_2 = d_ * self.dead + l2 * self.live + max(s2 * self.snow, 0.4 * self.wind)
        c_3 = d_ * self.dead + 1.5 * self.snow + max(l3 * self.live, 0.4 * self.wind)
        c_4 = d_ * self.dead + 1.4 * self.wind + max(l4 * self.live, s4 * self.snow)
        c_5 = self.dead + self.earthquake + l5 * self.live + s5 * self.snow
        elu = max(c_1, c_2, c_3, c_4, c_5)
        return elu

    def elts(self):
        pass


# tests
def main():
    dead = LimitStatesDesign(dead=1).elu()
    res = 1.4
    if dead != res:
        print("dead -> FAILED")
        print(f"result = {dead}")
        print(f"expected = {res}\n")
    else:
        print("dead -> PASSED\n")

    live = LimitStatesDesign(live=1).elu()
    res = 1.5
    if live != res:
        print("live -> FAILED")
        print(f"result = {live}")
        print(f"expected = {res}\n")
    else:
        print("live -> PASSED\n")

    snow = LimitStatesDesign(snow=1).elu()
    res = 1.5
    if snow != res:
        print("snow -> FAILED")
        print(f"result = {snow}")
        print(f"expected = {res}\n")
    else:
        print("snow -> PASSED\n")

    wind = LimitStatesDesign(wind=1).elu()
    res = 1.4
    if wind != res:
        print("wind -> FAILED")
        print(f"result = {wind}")
        print(f"expected = {res}\n")
    else:
        print("wind -> PASSED\n")

    earthquake = LimitStatesDesign(earthquake=1).elu()
    res = 1
    if earthquake != res:
        print("earthquake -> FAILED")
        print(f"result = {earthquake}")
        print(f"expected = {res}\n")
    else:
        print("earthquake -> PASSED\n")


if __name__ == "__main__":
    main()
