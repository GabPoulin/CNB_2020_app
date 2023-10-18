"""
Script pour effectuer les calculs selon la section
4.1. Charges et methodes de calculs du CNB-2020.
"""


class LimitStatesDesign:
    """Calcul de ELU ou ELTS selon la section 4.1.3."""

    def __init__(
        self,
        dead=0,
        live=0,
        snow=0,
        wind=0,
        earthquake=0,
        storage_area="no",
        exterior_area="no",
        car_access="no",
    ):
        self.d = dead
        self.l = live
        self.s = snow
        self.w = wind
        self.e = earthquake
        self.storage = storage_area
        self.ext = exterior_area
        self.car = car_access

    def elu(self, counter_d="no", liquid_l="no", h_s=0):
        """Calcul l'ELU selon le Tableau 4.1.3.2.-A du CNB-2020.

        Args:
            counter_d (optional): Charge permanente pondérée contraire. Defaults to "no".
            liquid_l (optional): Coeff. de surcharge réduit pour liquides. Defaults to "no".
            h_s (optional): Profondeur du sol, en m, supporté par la structure. Defaults to "no".

        Returns:
            float: État Limite Ultime
        """

        # Pondération sur D
        d1_factor = 1.4
        d_factor = 1.25
        if h_s > 0:
            d1_factor = 1.5  # 4.1.3.2. 9)
            d_factor = 1.5  # 4.1.3.2. 8)
            if h_s > 1.2:
                d_factor = max(1 + 0.6 / h_s, 1.25)  # 4.1.3.2. 8)
        if counter_d != "no":
            d_factor = 0.9  # 4.1.3.2. 5)

        # Pondération sur L
        pr_l_factor = 1.5
        if liquid_l != "no":
            pr_l_factor = 1.25  # 4.1.3.2. 6)
        co_l_factor = 0
        if self.storage != "no":
            co_l_factor = 0.5  # 4.1.3.2. 7)

        # 4.1.5.5.
        co_ls_factor = 1
        co_l5_factor = 1
        co_s5_factor = 1
        co_ls_red_factor = 1
        co_l5_red_factor = 1
        co_s5_red_factor = 1
        if self.ext != "no":
            if self.car == "no":
                co_ls_factor = 0
                if (0.5 + co_l_factor) * self.l < 0.25 * self.s:
                    co_l5_factor = 0
                else:
                    co_s5_factor = 0
            co_ls_red_factor = 0.2
            co_l5_red_factor = 0.4
            co_s5_red_factor = 0.8

        # Combinaisons de charges
        cas_1 = d1_factor * self.d
        cas_2 = (
            d_factor * self.d
            + pr_l_factor * self.l
            + max(self.s * co_ls_factor * co_ls_red_factor, 0.4 * self.w)
        )
        cas_3 = (
            d_factor * self.d
            + 1.5 * self.s
            + max(
                (1 + co_l_factor) * self.l * co_ls_factor * co_ls_red_factor,
                0.4 * self.w,
            )
        )
        cas_4 = (
            d_factor * self.d
            + 1.4 * self.w
            + max((0.5 + co_l_factor) * self.l, 0.5 * self.s)
        )
        cas_5 = (
            self.d
            + self.e
            + (0.5 + co_l_factor) * self.l * co_l5_red_factor * co_l5_factor
            + 0.25 * self.s * co_s5_red_factor * co_s5_factor
        )

        # ELU max
        elu = max(cas_1, cas_2, cas_3, cas_4, cas_5)

        return elu

    def elts(self):
        pass


# tests
if __name__ == "__main__":
    plancher_test = LimitStatesDesign(dead=1, live=1)
    print(f"---test plancher---\n{plancher_test.elu()}")

    parking_test = LimitStatesDesign(
        dead=5,
        live=4.8,
        snow=3,
        storage_area="no",
        exterior_area="yes",
        car_access="yes",
    )
    print(f"---test parking---\n{parking_test.elu(h_s=1)}")
