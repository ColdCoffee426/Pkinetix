"""
Coordinates pharmacokinetic result calculations.

Individual PK parameters are delegated to dedicated
calculator modules.
"""

from app.models.analysis_result import AnalysisResult
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

    def calculate(self) -> AnalysisResult:
        """
        Calculate all currently implemented
        pharmacokinetic parameters.
        """

        result = AnalysisResult()

        cmax_observation = calculate_cmax(
            self.project.observations
        )

        if cmax_observation is not None:
            result.cmax = cmax_observation.concentration
            result.tmax = calculate_tmax(
                cmax_observation
            )

        return result