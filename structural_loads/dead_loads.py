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
Base = declarative_base()


@dataclass
class DeadLoadsData(Base):
    """Fait référence à la table dead_loads de loads.db."""

    __tablename__ = "dead_loads"
    category: str = Column("category", TEXT)
    material: str = Column("material", TEXT, primary_key=True)
    load: str = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    reference: str = Column("reference", TEXT)


engine = create_engine("sqlite:///loads.db")
Base.metadata.create_all(bind=engine)

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

    def materials_weight(self):
        """Indique le poids (en kPa) des matériaux."""

    def calculate(self, add_partitions=False, add_weight=0):
        """4.1.4.1. Charge permanente.
            Additionne le poids de tous les matériaux supportés de façon permanente par l'élément.

        Args:
            add_partitions (optional): Poids des cloisons. Defaults to False.
            add_weight (optional): Poids additionnel (kPa). Defaults to 0.

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
    """tests pour la classe DeadLoads"""
    print("")

    test = DeadLoads(1, 4).calculate(True, 1)
    expected_result = 7
    if test != expected_result:
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
    # pass

### END ###
