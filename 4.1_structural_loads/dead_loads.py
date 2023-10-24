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
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


# DB CONNECTION
@dataclass
class DeadLoadsTable(declarative_base()):
    """Se connecte à la table dead_loads de loads.db."""

    __tablename__ = "dead_loads"
    material: str = Column("material", TEXT, primary_key=True)
    load: str = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    session = sessionmaker(create_engine("sqlite:///loads.db"))()


# CODE
@dataclass
class DeadLoads:
    """4.1.4. Charge permanente.

    Args:
        materials: Liste des matériaux qui composent l'élément.
        member_name: Nom de l'élément structural.
    """

    materials: list[str]
    member_name: str = "matériaux"
    member_name = member_name.title()

    def member_load(self, print_table=False):
        """Calcul la poids total des matériaux qui composent l'élément.

        Args:
            print_table: Créé un tableau pour indiquer le poids de chaque matériau.
        Returns:
            Poids total de l'élément structural.
        """

        total = 0
        table = ""
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
                thickness = float(
                    input(f"{self.member_name}: Épaisseur pour {mat.material} en mm: ")
                )
                load *= thickness
                thickness = f" {int(thickness)}mm"
                if unit == "N/m3":
                    load /= 1000
            load /= 1000
            if print_table:
                table += f"{mat.material}{thickness}|{round(load,2)} kPa\n"
            total += load
        total = round(total, 2)

        if print_table:
            with open(file="member_loads.md", mode="a", encoding="utf-8") as md_file:
                md_file.write(
                    f"{self.member_name}| |\n"
                    + "-|-\n"
                    + table
                    + f"__Total__:|__{total}__ __kPa__\n"
                    + "---\n"
                )

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

        dead_loads = additional_loads
        if add_partitions:
            dead_loads += 1
        dead_loads += round(self.member_load(), 2)

        return dead_loads


# TESTS
def tests():
    """Tests pour la classe DeadLoads."""

    liste1 = [
        "Bois de feuillus 20mm",
        "É-P-S 19mm",
        "2x10 à 16po",
        "Liens continus",
        "Panneau de gypse 12mm",
    ]
    test_sum_dead_loads = DeadLoads(liste1).sum_dead_loads(True, 2)
    expected_result = 3.51

    if test_sum_dead_loads != expected_result:
        print("test_sum_dead_loads -> FAILED")
        print("result = ", test_sum_dead_loads)
        print("expected = ", expected_result)
    else:
        print("test_sum_dead_loads -> PASSED")

    test_member_load = DeadLoads(liste1).member_load(False)
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
    test_print_table = DeadLoads(toiture).member_load(True)
    expected_result = 0.4
    if test_print_table != expected_result:
        print("test_print_table -> FAILED")
        print("result = ", test_print_table)
        print("expected = ", expected_result)
    else:
        print("test_print_table -> PASSED")


# RUN FILE
if __name__ == "__main__":
    print("------START_TESTS------")
    tests()
    print("-------END_TESTS-------")
    clt = ["E2 12%"]
    DeadLoads(clt).member_load(True)

# END
