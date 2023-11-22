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
from dead_loads import DeadLoads
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
    snow_rain: float = Column("snow_rain", REAL)
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
        dome: Toit à 2 versants ou en dôme.
        drifting_distance: Distance avec le toit adjacent plus élevé (m).
        exposed_to_wind: Bâtiment exposé au vent sur toutes ses faces.
        importance: Catégorie de risque ("Faible", "Normal", "Élevé", "Protection civile").
        limit_state: Spécifier ("ÉLU", "ÉLTS").
        meltwater: Écoulement des eaux de fonte depuis un toit adjacent.
        north_area: Région située au nord de la limite des arbres.
        projections_height: Hauteur de l'élément hors toit (m).
        rain_accumulation: Possibilité d'ccumulation d'eaux pluviales.
        rural_area: Région rurale.
        sliding: Glissement provenant d'un toit adjacent.
        slippery_roof: Toit glissant sans obstruction.
        valley: Accumulation aux noues.
        wind_obstructions_distance: Distance avec l'obstacle (m).
        wind_obstructions_height: Hauteur de l'obstacle (m).
    """

    location: str
    roof_height: float
    roof_larger_dimension: float
    roof_smaller_dimension: float
    slope: float

    dome: bool = False
    drifting_distance: float = 10
    exposed_to_wind: bool = False
    importance: str = "Normal"
    limit_state: str = "ÉLU"
    meltwater: bool = False
    north_area: bool = False  # inclure dans db
    projections_height: float = 0
    rain_accumulation: bool = False
    rural_area: bool = False  # inclure dans db
    sliding: bool = False
    slippery_roof: bool = False
    valley: bool = False
    wind_obstructions_distance: float = 0
    wind_obstructions_height: float = 0

    def _get_climate_info(self):
        """Récupère les données climatiques de loads.db pour l'emplacement choisi."""

        return (
            ClimaticDataTable.session.query(ClimaticDataTable)
            .filter(ClimaticDataTable.location == self.location)
            .first()
        )

    def specified_load(self):
        """4.1.6.1. Charge spécifiée due à la pluie, ou à la neige et à la pluie qui l'accompagne."""

        return max(self._specified_snow_load(), self._specified_rain_load())

    def _specified_snow_load(self):
        """4.1.6.2. - S: Charge spécifiée due à la neige."""

        importance_factor = self._importance_factor()
        snow_load = self._get_climate_info().snow
        basic_factor = self._basic_factor()
        wind_factor = self._wind_factor()
        slope_factor = self._slope_factor()
        accumulation_factor = self._accumulation_factor()
        print("Ca =", accumulation_factor)
        rain_load = min(
            self._get_climate_info().snow_rain,
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
            b = self.wind_obstructions_height > 0
            c = self.drifting_distance > 5
            d = not self.sliding
            if a and b and c and d:
                if self.north_area:
                    cw = 0.5
                elif self.rural_area:
                    cw = 0.75
                else:
                    b = False

                if b:
                    d = self.wind_obstructions_distance
                    h = self.wind_obstructions_height
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

        if self.drifting_distance <= 5:  # 4.1.6.5.-6.-8.
            ca_a = 1
            ca = max(ca, ca_a)

        if self.projections_height > 0:  # 4.1.6.7.-8.
            ca_b = 1
            ca = max(ca, ca_b)

        if self.dome:  # 4.1.6.9.-10.
            ca_c = 1
            ca = max(ca, ca_c)

        if self.sliding:  # 4.1.6.11.
            ca_d = 1
            ca = max(ca, ca_d)

        if self.valley:  # 4.1.6.12.
            ca_e = 1
            ca = max(ca, ca_e)

        if self.meltwater:
            ca_f = 1
            ca = max(ca, ca_f)

        return ca

    def _specified_rain_load(self):
        specified_load = 1

        return specified_load

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
        drifting_distance=10,
        exposed_to_wind=True,
        importance="Normal",
        limit_state="ÉLU",
        north_area=False,
        rural_area=True,
        slippery_roof=True,
        wind_obstructions_distance=1,
        wind_obstructions_height=0.86,
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
