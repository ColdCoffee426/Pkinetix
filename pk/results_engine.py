#this file will be coordinating all the calculations
#will import all calculatios from NCA

from app.models.project import Project
from pk.nca.cmax import calculate as calculate_cmax
from pk.nca.tmax import calculate as calculate_tmax

class ResultsEngine:
    """
    Coordinates pharmacokinetic result calculations.

    Individual PK parameters are delegated to dedicated
    calculator modules.
    """

    def __init__(self, project: Project) -> None:
        self.project = project

    def calculate(self) -> dict[str, float | None]:

        cmax_observation = calculate_cmax(
            self.project.observations
        )

        cmax = None
        tmax = None

        if cmax_observation is not None:
            cmax = cmax_observation.concentration
            tmax = calculate_tmax(cmax_observation)

        return {
            "Cmax": cmax,
            "Tmax": tmax,
            "Lambda_z": None,
            "Half-life": None,
            "AUC0-t": None,
            "AUC0-inf": None,
            "AUMC": None,
            "MRT": None,
            "Clearance": None,
            "Vz": None,
        }