"""
Coordinates pharmacokinetic result calculations.

Individual PK parameters are delegated to dedicated
calculator modules.
"""

from app.models.analysis_result import AnalysisResult
from app.models.project import Project
from pk.nca.auc import calculate as calculate_auc
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
        result = AnalysisResult()

        observations = self.project.observations

        cmax_observation = calculate_cmax(observations)

        if cmax_observation is not None:
            result.cmax = cmax_observation.concentration
            result.tmax = calculate_tmax(cmax_observation)

        result.auc_0_t = calculate_auc(observations)

        return result