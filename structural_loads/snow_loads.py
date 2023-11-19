"""

CNB 2020: Partie 4. Règles de calcul.
Section 4.1. Charges et méthodes de calcul.
-----------------------------------------------

4.1.6. Charge due à la neige et à la pluie.

    desc.
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
    """Se connecte à la table X de loads.db."""

    __tablename__ = "X"
    XX: str = Column("XX", TEXT, primary_key=True)
    XXX: float = Column("XXX", REAL)
    engine = create_engine("sqlite:///loads.db")
    Session = sessionmaker(engine)
    session = Session()


# CODE
@dataclass
class SnowLoads:
    """4.1.6. Charge due à la neige et à la pluie.

    Args:
        arg: desc.
    """

    arg: str = "default value"

    def snow_load(self):
        """4.1.6.2. Charge spécifiée due à la neige.

        Args:
            arg: desc.
        """

        Is = importance_factor
        Ss = snow_load
        Cb = basic_factor
        Cw = wind_factor
        Cs = slope_factor
        Ca = accumulation_factor
        Sr = rain_load

        S = Is * (Ss * (Cb * Cw * Cs * Ca) + Sr)

        return S


# TESTS
def tests():
    """tests pour la classe SnowLoads."""

    test1 = SnowLoads().func_name()
    expected_result = None
    if test1 != expected_result:
        print("test1 -> FAILED")
        print("result = ", test1)
        print("expected = ", expected_result)
    else:
        print("test1 -> PASSED")


# RUN FILE
if __name__ == "__main__":
    print("------START_TESTS------")
    tests()
    print("-------END_TESTS-------")

# END
