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
class ClimaticDataTable(declarative_base()):
    """Se connecte à la table climatic_data de loads.db."""

    __tablename__ = "climatic_data"
    location: str = Column("location", TEXT, primary_key=True)
    snow: float = Column("snow", REAL)
    rain: float = Column("rain", REAL)
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
        location: Emplacement du bâtiment.
    """

    location: str
    importance: str = "Normal"
    limit_state: str = "ÉLU"

    def specified_load(self):
        """4.1.6.2. Charge spécifiée due à la neige."""

        importance_factor = self._importance_factor()
        snow_load = self._get_climate_info().snow
        basic_factor = self._basic_factor()
        wind_factor = self._wind_factor()
        slope_factor = self._slope_factor()
        accumulation_factor = self._accumulation_factor()
        rain_load = min(
            self._get_climate_info().rain,
            snow_load
            * (basic_factor * wind_factor * slope_factor * accumulation_factor),
        )

        specified_load = importance_factor * (
            snow_load
            * (basic_factor * wind_factor * slope_factor * accumulation_factor)
            + rain_load
        )

        return round(specified_load, 2)

    def _importance_factor(self):
        """Tableau 4.1.6.2.-A. - Is: coefficient de risque de la charge due à la neige."""

        factor = 1
        if self.importance == "Faible":
            factor = 0.8
        if self.importance == "Élevé":
            factor = 1.15
        if self.importance == "Protection civile":
            factor = 1.25
        if self.limit_state == "ÉLTS":
            factor = 0.9

        return factor

    def _basic_factor(self):
        """4.1.6.2.2). - Cb: coefficient de base de charge de neige sur le toit."""

        factor = 1

        return 1

    def _wind_factor(self):
        """4.1.6.2.3) et 4). - Cw: coefficient d'exposition au vent."""

        return 1

    def _slope_factor(self):
        """4.1.6.2.5) à 7). - Cs: coefficient de pente."""

        return 1

    def _accumulation_factor(self):
        """4.1.6.2.8). - Ca: coefficient d'accumulation."""

        return 1

    def _get_climate_info(self):
        """Récupère les données climatiques de loads.db pour l'emplacement choisi."""

        return (
            ClimaticDataTable.session.query(ClimaticDataTable)
            .filter(ClimaticDataTable.location == self.location)
            .first()
        )

    def _snow_specific_weight(self):
        """4.1.6.13. - γ: poids spécifique de la neige."""

        return min(4, 0.43 * self._get_climate_info().snow + 2.2)


# TESTS
def tests():
    """tests pour la classe SnowLoads."""

    print("------START_TESTS------")

    test1 = SnowLoads(
        location="Gaspé",
        importance="Normal",
        limit_state="ÉLU",
    ).specified_load()
    expected_result = 4.9
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
