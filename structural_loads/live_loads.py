"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.5. Surcharges dues à l'usage.

    Détermine la surcharge spécifiée selon l'usage prévu.
        1- Méthode des surcharges uniformément réparties 4.1.5.3.
        2- Méthode des surcharges concentrées 4.1.5.9.
____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

# IMPORTS
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL, INTEGER


# DB CONNECTION
@dataclass
class LiveLoadsTable(declarative_base()):
    """Se connecte à la table live_loads de loads.db."""

    __tablename__ = "live_loads"
    use: str = Column("use", TEXT, primary_key=True)
    uniform: float = Column("uniform", REAL)
    concentrated: float = Column("concentrated", REAL)
    area_x: int = Column("area (x)", INTEGER)
    area_y: int = Column("area (y)", INTEGER)
    engine = create_engine("sqlite:///loads.db")
    Session = sessionmaker(engine)
    session = Session()


# CODE
@dataclass
class LiveLoads:
    """4.1.5. Surcharges dues à l'usage.

    Args:
        use: Usage prévue.
        importance: Catégorie de risque.
    """

    use: str
    importance: str = "Normal"

    def _get_info(self):
        """Récupère les informations de loads.db pour l'usage prévu."""

        return (
            LiveLoadsTable.session.query(LiveLoadsTable)
            .filter(LiveLoadsTable.use == self.use)
            .first()
        )

    def _low_importance_factor(self, load):
        """Dans le cas des bâtiments de la catégorie risque faible, applique un coefficient de 0.8."""

        if self.importance == "Faible":
            load *= 0.8

        return round(load, 1)

    def uniform_load(self, width: float, length: float, reinforced_slab=False):
        """4.1.5.3. Surcharge totale et surcharge partielle.

        Args:
            width: Largeur de surface (m).
            length: Longueur de surface (m).

            reinforced_slab: 'True' si la surface est une dalle armée.
        """

        load = self._get_info().uniform
        area = width * length

        if self.use == "Salle à manger":
            load = self._dining_area(load, area)

        reduction_factor, reduction_message = self._tributary_area(
            reinforced_slab, load, area
        )
        load *= reduction_factor

        return self._low_importance_factor(load), reduction_message

    def _dining_area(self, load, area):
        """4.1.5.6. Salles à Manger."""

        if area <= 100:
            load = 2.4

        return load

    def _tributary_area(self, reinforced_slab, load, area):
        """4.1.5.8. Surface Trubutaire."""

        assembly_occupancy = (
            "Salle de classe et d'audience",
            "Lieu de réunion (c)",
            "Lieu de réunion (d)",
            "Toit",
        )
        use_A = (
            "Stockage",
            "Équipement et local technique",
            "Bibliothèque (rayonnage)",
            "Entrepôt",
            "Commerce de gros détail",
            "Garage (véhicules <= 4000 kg)",
            "Garage (4000 kg < véhicules <= 9000 kg)",
            "Garage (véhicules > 9000 kg)",
            "Lieu de réunion (a)",
            "Vomitoire, issue, hall et corridor",
            "Mezzanine et passerelle",
            "Usine",
            "Salle à manger",
        )

        reduction = False
        if not reinforced_slab:
            if self.use not in assembly_occupancy:
                if self.use == "Salle à manger":
                    if load >= 4.8:
                        reduction = True
                else:
                    reduction = True

        factor = 1
        A = area
        B = area
        if reduction:
            if self.use in use_A:
                if area > 80:
                    factor = 0.5 + (20 / A) ** 0.5
            else:
                if area > 20:
                    factor = 0.3 + (9.8 / B) ** 0.5

        message = "Aucun coefficient de réduction de surface tributaire n'est appliqué."
        if factor != 1:
            message = f"Un coefficient de {round(factor,2)} est appliqué à la surface tributaire."

        return factor, message

    def concentrated_load(self):
        """4.1.5.9. Surcharges concentrées"""

        load = 0
        message = "Aucune charge concentrée requise."
        if self._get_info().concentrated:
            load = self._get_info().concentrated
            area_x = self._get_info().area_x
            area_y = self._get_info().area_y
            message = f"Surface de {area_x}mm x {area_y}mm soumise à la charge."

        return self._low_importance_factor(load), message


# TESTS
def tests():
    """tests pour la classe LiveLoads."""

    print("------START_TESTS------")

    garage = "Garage (véhicules > 9000 kg)"
    salle_a_manger = "Salle à manger"
    faible = "Faible"

    test1_uniform_load = LiveLoads(garage, faible).uniform_load(5, 10, True)
    expected_result = (
        9.6,
        "Aucun coefficient de réduction de surface tributaire n'est appliqué.",
    )
    if test1_uniform_load != expected_result:
        print("test1_uniform_load -> FAILED")
        print("result = ", test1_uniform_load)
        print("expected = ", expected_result)
    else:
        print("test1_uniform_load -> PASSED")

    test2_uniform_load = LiveLoads(salle_a_manger).uniform_load(10, 20)
    expected_result = (
        3.9,
        "Un coefficient de 0.82 est appliqué à la surface tributaire.",
    )
    if test2_uniform_load != expected_result:
        print("test2_uniform_load -> FAILED")
        print("result = ", test2_uniform_load)
        print("expected = ", expected_result)
    else:
        print("test2_uniform_load -> PASSED")

    test3_concentrated_load = LiveLoads(garage).concentrated_load()
    expected_result = 54, "Surface de 250mm x 600mm soumise à la charge."
    if test3_concentrated_load != expected_result:
        print("test3_concentrated_load -> FAILED")
        print("result = ", test3_concentrated_load)
        print("expected = ", expected_result)
    else:
        print("test3_concentrated_load -> PASSED")

    test4_concentrated_load = LiveLoads(salle_a_manger).concentrated_load()
    expected_result = 0, "Aucune charge concentrée requise."
    if test4_concentrated_load != expected_result:
        print("test4_concentrated_load -> FAILED")
        print("result = ", test4_concentrated_load)
        print("expected = ", expected_result)
    else:
        print("test4_concentrated_load -> PASSED")

    print("-------END_TESTS-------")


# RUN FILE
if __name__ == "__main__":
    tests()

# END
