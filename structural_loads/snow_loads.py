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
from math import exp
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
        location: Emplacement du bâtiment.
        roof_height: Hauteur moyenne du toit au-dessus du niveau moyen du sol (m).
        roof_larger_dimension: Plus grande dimension horizontale du toit (m).
        roof_smaller_dimension: Plus petite dimension horizontale du toit (m).
        slope: Pente du toit (°).

    Optional:
        drifting: Accumulation de neige provenant de toit adjacents.
        exposed_to_wind: Bâtiment exposé au vent sur toutes ses faces.
        importance: Catégorie de risque ("Faible", "Normal", "Élevé", "Protection civile").
        limit_state: Spécifier ("ÉLU", "ÉLTS").
        north_area: région située au nord de la limite des arbres.
        obstructions_distance: Distance de l'obstacle (m).
        obstructions_height: Hauteur de l'obstacle (m).
        rural_area: Région rurale.
        slippery_roof: Toit glissant sans obstruction.
    """

    location: str
    roof_height: float
    roof_larger_dimension: float
    roof_smaller_dimension: float
    slope: float

    drifting: bool = False
    exposed_to_wind: bool = False
    importance: str = "Normal"
    limit_state: str = "ÉLU"
    north_area: bool = False  # inclure dans db
    obstructions_distance: float = 0
    obstructions_height: float = 0
    rural_area: bool = False  # inclure dans db
    slippery_roof: bool = False

    def _get_climate_info(self):
        """Récupère les données climatiques de loads.db pour l'emplacement choisi."""

        return (
            ClimaticDataTable.session.query(ClimaticDataTable)
            .filter(ClimaticDataTable.location == self.location)
            .first()
        )

    def specified_load(self):
        """4.1.6.2. - S: Charge spécifiée due à la neige."""

        importance_factor = self._importance_factor()
        print("Is =", importance_factor)
        snow_load = self._get_climate_info().snow
        print("Ss =", snow_load)
        basic_factor = self._basic_factor()
        print("Cb =", basic_factor)
        wind_factor = self._wind_factor()
        print("Cw =", wind_factor)
        slope_factor = self._slope_factor()
        print("Cs =", slope_factor)
        accumulation_factor = self._accumulation_factor()
        print("Ca =", accumulation_factor)
        rain_load = min(
            self._get_climate_info().rain,
            snow_load
            * (basic_factor * wind_factor * slope_factor * accumulation_factor),
        )
        print("Sr =", rain_load)

        specified_load = importance_factor * (
            snow_load
            * (basic_factor * wind_factor * slope_factor * accumulation_factor)
            + rain_load
        )
        print("S = ", specified_load)

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

        cb = 1

        ss = self._get_climate_info().snow
        gamma = self._snow_specific_weight()
        if self.roof_height >= 1 + (ss / gamma):
            w = self.roof_smaller_dimension
            l = self.roof_larger_dimension
            lc = 2 * w - w**2 / l

            cw = self._wind_factor()
            if lc <= 70 / cw**2:
                cb = 0.8
            else:
                cb = (1 / cw) * (1 - (1 - 0.8 * cw) * exp(-(lc * cw**2 - 70) / 100))

        return cb

    def _wind_factor(self):
        """4.1.6.2.3) et 4). - Cw: coefficient d'exposition au vent."""

        cw = 1

        if self.importance in ("Faible", "Normal"):
            a = self.exposed_to_wind
            b = self.obstructions_height > 0
            c = not self.drifting
            if a and b and c:
                if self.north_area:
                    cw = 0.5
                elif self.rural_area:
                    cw = 0.75
                else:
                    b = False

                if b:
                    d = self.obstructions_distance
                    h = self.obstructions_height
                    ss = self._get_climate_info().snow
                    gamma = self._snow_specific_weight()
                    if d < 10 * (h - cw * ss / gamma):
                        cw = 1

        return cw

    def _slope_factor(self):
        """4.1.6.2.5) à 7). - Cs: coefficient de pente."""

        alpha = self.slope
        if not self.slippery_roof:
            if alpha <= 30:
                cs = 1
            elif alpha <= 70:
                cs = (70 - alpha) / 40
            else:
                cs = 0

        else:
            if alpha <= 15:
                cs = 1
            elif alpha <= 60:
                cs = (60 - alpha) / 45
            else:
                cs = 0

        if self._accumulation_factor() > 1:
            cs = 1

        return cs

    def _accumulation_factor(self):
        """4.1.6.2.8). - Ca: coefficient d'accumulation."""

        ca = 1

        return ca

    def _snow_specific_weight(self):
        """4.1.6.13. - γ: poids spécifique de la neige."""

        gamma = min(4, 0.43 * self._get_climate_info().snow + 2.2)

        return gamma


# TESTS
def tests():
    """tests pour la classe SnowLoads."""

    print("------START_TESTS------")

    test1 = SnowLoads(
        location="Gaspé",
        roof_height=5,
        roof_larger_dimension=5,
        roof_smaller_dimension=5,
        slope=25,
        drifting=False,
        exposed_to_wind=True,
        importance="Normal",
        limit_state="ÉLU",
        north_area=False,
        obstructions_distance=1,
        obstructions_height=0.86,
        rural_area=True,
        slippery_roof=True,
    ).specified_load()
    expected_result = 2.61
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
