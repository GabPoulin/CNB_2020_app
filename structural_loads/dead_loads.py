"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.4. Charge permanente.

    Effectue le calcul pour la charge permanente à partir du poids de différents matériaux.
____________________________________________________________________________________________________
    
    
    auteur: GabPoulin
    email: poulin33@me.com
    
====================================================================================================
"""

# IMPORTS
from dataclasses import dataclass
from tkinter import filedialog
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


# DB CONNECTION
@dataclass
class DeadLoadsTable(declarative_base()):
    """Se connecte à la table dead_loads de loads.db."""

    __tablename__ = "dead_loads"
    material: str = Column("material", TEXT, primary_key=True)
    load: float = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    session = sessionmaker(create_engine("sqlite:///loads.db"))()


# CODE
@dataclass
class DeadLoads:
    """4.1.4. Charge permanente.

    Args:
        materials: Liste des matériaux qui composent l'élément.
    """

    materials: list[str] = ()

    def member_load(self):
        """Calcul la poids total des matériaux qui composent l'élément.

        Returns:
            Poids total de l'élément structural.
        """

        total = 0
        for item in self.materials:
            mat = (
                DeadLoadsTable.session.query(DeadLoadsTable)
                .filter(DeadLoadsTable.material == item)
                .first()
            )
            unit = mat.unit
            load = mat.load
            thickness = ""
            if unit in ("N/m3", "N/m2/mm"):
                thickness = float(input(f"Épaisseur pour {mat.material} en mm: "))
                load *= thickness
                if unit == "N/m3":
                    load /= 1000
            load /= 1000
            total += load
        total = round(total, 2)

        return total

    def sum_dead_loads(self, add_partitions=False, additional_loads=0):
        """4.1.4.1. Charge permanente.
            Calcul le poids des matériaux, des cloisons et de tout autre charges destinés à être
            supportés de façon permanente par l'élément structural.

        Args:
            add_partitions: Ajoute 1 kPa pour le poids des cloisons.
            additional_loads: Poids additionnel (en kPa).
        Returns:
            Charge permanente.
        """

        d = additional_loads
        if add_partitions:
            d += 1
        d += round(self.member_load(), 2)

        return d


# TESTS
def tests():
    """Tests pour la classe DeadLoads."""

    print("------START_TESTS------")

    floor = [
        "Bois de feuillus 20mm",
        "É-P-S 19mm",
        "2x10 à 16po",
        "Liens continus",
        "Panneau de gypse 12mm",
    ]
    test_sum_dead_loads = DeadLoads(floor).sum_dead_loads(True, 2)
    expected_result = 3.51

    if test_sum_dead_loads != expected_result:
        print("test_sum_dead_loads -> FAILED")
        print("result = ", test_sum_dead_loads)
        print("expected = ", expected_result)
    else:
        print("test_sum_dead_loads -> PASSED")

    test_member_load = DeadLoads(floor).member_load()
    expected_result = 0.51
    if test_member_load != expected_result:
        print("test_member_load -> FAILED")
        print("result = ", test_member_load)
        print("expected = ", expected_result)
    else:
        print("test_member_load -> PASSED")

    toiture = [
        "Bardeaux d'asphalte",
        "Membrane caoutchoutée",
        "2x6 à 24po",
        "2x4 à 24po",
        "2x8 à 24po",
        "Liens continus",
        "Panneau de gypse 12mm",
    ]
    test2_member_load = DeadLoads(toiture).member_load()
    expected_result = 0.4
    if test2_member_load != expected_result:
        print("test2_member_load -> FAILED")
        print("result = ", test2_member_load)
        print("expected = ", expected_result)
    else:
        print("test2_member_load -> PASSED")

    test3_member_load = DeadLoads(["Eau douce"]).member_load()
    print(test3_member_load)

    print("-------END_TESTS-------")


# RUN FILE
if __name__ == "__main__":
    tests()

# END
