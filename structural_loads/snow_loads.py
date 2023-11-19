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
class XLoadsTable(declarative_base()):
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
        importance: Catégorie de risque ("Faible", "Normal", "Élevé", "Protection civile").
        limit_state: Spécifier ("ÉLU", "ÉLTS").
    """

    importance: str = "Normal"
    limit_state: str = "ÉLU"

    def specified_snow_load(self):
        """4.1.6.2. Charge spécifiée due à la neige.

        Args:
            arg: desc.
        """

        importance_factor = self._importance_factor()
        snow_load = self._snow_load()
        basic_factor = self._basic_factor()
        wind_factor = self._wind_factor()
        slope_factor = self._slope_factor()
        accumulation_factor = self._accumulation_factor()
        rain_load = self._rain_load()

        specified_snow_load = importance_factor * (
            snow_load
            * (basic_factor * wind_factor * slope_factor * accumulation_factor)
            + rain_load
        )

        return specified_snow_load

    def _importance_factor(self):
        """Tableau 4.1.6.2.-A. Coefficient de risque de la charge due à la neige, Is"""

        uls_factor = 1
        sls_factor = 0.9

        if self.importance == "Faible":
            uls_factor = 0.8

        return uls_factor, sls_factor

    def _snow_load(self):
        return 1

    def _basic_factor(self):
        return 1

    def _wind_factor(self):
        return 1

    def _slope_factor(self):
        return 1

    def _accumulation_factor(self):
        return 1

    def _rain_load(self):
        return 1


# TESTS
def tests():
    """tests pour la classe SnowLoads."""

    print("------START_TESTS------")

    test1 = SnowLoads().specified_snow_load()
    expected_result = 2
    if test1 != expected_result:
        print("test1 -> FAILED")
        print("result = ", test1)
        print("expected = ", expected_result)
    else:
        print("test1 -> PASSED")

    print("-------END_TESTS-------")


# RUN FILE
if __name__ == "__main__":
    tests()

# END
