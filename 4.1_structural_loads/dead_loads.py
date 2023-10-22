"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.4. Charge permanente.

    Effectue le calcul pour la charge permanente à partir des données de masse de différents
    matériaux.
____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### IMPORTS ###
from dataclasses import dataclass
from simple_colors import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


### DB MANAGEMENT ###
@dataclass
class DeadLoadsTable(declarative_base()):
    """Fait référence à la table dead_loads de loads.db."""

    __tablename__ = "dead_loads"
    category: str = Column("category", TEXT)
    material: str = Column("material", TEXT, primary_key=True)
    load: str = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    reference: str = Column("reference", TEXT)

    engine = create_engine("sqlite:///loads.db")
    Session = sessionmaker(engine)
    session = Session()


### CODE ###
class DeadLoads:
    """4.1.4. Charge permanente."""

    def __init__(self, materials: list[str]):
        """4.1.4. Charge permanente.

        Args:
            materials: Liste des matériaux.
        """
        self.materials = materials

    def sum_materials_loads(self, print_table=False):
        """Calcul la charge totale des matériaux.

        Args:
            print_table: Affiche un tableau des charges avec le poids chaque matériau.
                Defaults to False.

        Returns:
            int: Charge totale.
        """

        total = 0
        table = ""
        for item in self.materials:
            mat = (
                DeadLoadsTable.session.query(DeadLoadsTable)
                .filter(DeadLoadsTable.material == item)
                .first()
            )
            load = mat.load
            unit = mat.unit

            if unit in ("N/m3", "N/m2/mm"):
                thickness = float(input(f"Épaisseur pour {mat.material} en mm: "))
                load *= thickness
                if unit == "N/m3":
                    load /= 1000
            load /= 1000

            if print_table:
                if unit in ("N/m3", "N/m2/mm"):
                    table += (
                        f"\n{mat.material} {int(thickness)}mm ---- {round(load,2)} kPa"
                    )
                else:
                    table += f"\n{mat.material} ---- {round(load,2)} kPa"

            total += load
        total = round(total, 2)

        if print_table:
            print()
            print(cyan("Charges permanentes:"))
            print("============================================================", table)
            print("============================================================")
            print("Total:", cyan(f"{total} kPa"))
            print("============================================================")
            print()

        return total

    def sum_dead_loads(self, add_partitions=False, additional_loads=0):
        """4.1.4.1. Charge permanente.
            Calcul le poids des matériaux, des cloisons et de tout autre charges destinés à être
            supportés de façon permanente par l'élément structural.

        Args:
            add_partitions: Poids des cloisons.
                Defaults to False.

            additional_loads: Poids additionnel (en kPa).
                Defaults to 0.

        Returns:
            int: Charge permanente
        """

        dead_loads = additional_loads
        if add_partitions:
            dead_loads += 1
        dead_loads += self.sum_materials_loads()
        dead_loads = round(dead_loads, 2)

        return dead_loads


### TESTS ###
def tests():
    """tests pour la classe DeadLoads."""
    print()

    liste1 = [
        "Bois de feuillus 20mm",
        "É-P-S 19mm",
        "2x10 à 16po",
        "Liens continus",
        "Panneau de gypse 12mm",
    ]
    test = DeadLoads(liste1).sum_dead_loads(True, 2)
    expected_result = 3.51
    if test != expected_result:
        print("DeadLoads.sum_dead_loads ->", red("FAILED"))
        print("result = ", test)
        print("expected = ", expected_result)
        print()
    else:
        print("DeadLoads.sum_dead_loads ->", green("GOOD"))
        print()

    test2 = DeadLoads(liste1).sum_materials_loads(False)
    expected_result = 0.51
    if test2 != expected_result:
        print("DeadLoads.sum_materials_loads ->", red("FAILED"))
        print("result = ", test2)
        print("expected = ", expected_result)
        print()
    else:
        print("DeadLoads.sum_materials_loads ->", green("GOOD"))
        print()

    DeadLoads(["Bois de feuillus 20mm", "Béton", "Contreplaqué"]).sum_materials_loads(
        True
    )


### RUN FILE ###
if __name__ == "__main__":
    print()
    print("------START_TESTS------")
    tests()
    print("-------END_TESTS-------")
    print()

### END ###
