"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.4. Charge permanente.


____________________________________________________________________________________________________
    

    auteur: GabPoulin
    email: poulin33@me.com

====================================================================================================
"""

### IMPORTS ###
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


### DB MANAGEMENT ###
@dataclass
class DeadLoadsTable(declarative_base()):
    """Fait référence à la table dead_loads de loads.db.

    Args:
        category: test

    """

    __tablename__ = "dead_loads"
    category: str = Column("category", TEXT)
    material: str = Column("material", TEXT, primary_key=True)
    load: str = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    reference: str = Column("reference", TEXT)

    engine = create_engine("sqlite:///loads.db")
    declarative_base().metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()


### CODE ###
class DeadLoads:
    """4.1.4. Charge permanente.

    Args:
        materials: Indiquer par leur nom tous les matériaux de construction incorporés au bâtiment
        et destinés à être supportés de façon permanente par l'élément.
    """

    def __init__(self, *materials: float):
        self.materials = materials

    def sum_materials_loads(self, individual_load=False):
        """Détermine le poids des matériaux en kPa.

        Returns:
            str: Charge morte total des matériaux

        """
        result = 0
        layers = 0
        for item in self.materials:
            layers += 1

            mat = (
                DeadLoadsTable.session.query(DeadLoadsTable)
                .filter(DeadLoadsTable.material == item)
                .first()
            )

            if mat.unit in ("N/m3", "N/m2/mm"):
                thickness = input(f"\tÉpaisseur de {mat.material} en mm = ")
                mat.load *= float(thickness)
                if mat.unit == "N/m3":
                    mat.load /= 1000

            mat.load /= 1000

            if individual_load:
                print(f"{layers}: {mat.material} = \t{round(mat.load,2)} kPa.")

            result += mat.load

        return result

    def calculate(self, add_partitions=False, add_weight=0):
        """4.1.4.1. Charge permanente.
            Additionne le poids de tous les matériaux supportés de façon permanente par l'élément.

        Args:
            add_partitions (optional): Poids des cloisons. Defaults to False.
            add_weight (optional): Poids additionnel (en kPa). Defaults to 0.

        Returns:
            int | float: Charge permanente
        """
        dead_loads = add_weight
        if add_partitions:
            dead_loads += 1
        for d in self.materials:
            dead_loads += d

        return dead_loads


### TESTS ###
def tests():
    """tests pour la classe DeadLoads.calculate"""
    print()

    test = DeadLoads(1, 4).calculate(True, 1)
    expected_result = 7
    if test != expected_result:
        print("DeadLoads.calculate -> FAILED")
        print("result = ", test)
        print("expected = ", expected_result)
        print()
    else:
        print("DeadLoads.calculate -> PASSED")
        print()

    DeadLoads(
        "Douglas-mélèze 12%", "Bois de feuillus 20mm", "Isolant en vrac"
    ).sum_materials_loads(True)


### RUN FILE ###
if __name__ == "__main__":
    print()
    print("------START_TESTS------")
    tests()
    print("-------END_TESTS-------")
    print()

    # pass

### END ###
