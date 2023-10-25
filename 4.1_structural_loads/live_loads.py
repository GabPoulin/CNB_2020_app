"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.5. X.

    description.
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
class LiveLoadsTable(declarative_base()):
    """Fait référence à la table x de loads.db."""

    __tablename__ = "live_loads"
    name: str = Column("name", TEXT, primary_key=True)
    load: str = Column("load", REAL)
    unit: str = Column("unit", TEXT)
    engine = create_engine("sqlite:///loads.db")
    Session = sessionmaker(engine)
    session = Session()


### CODE ###
class DeadLoads:
    """4.1.x. X."""

    pass


### TESTS ###
def tests():
    """tests pour la classe X."""
    pass


### RUN FILE ###
if __name__ == "__main__":
    pass

### END ###
