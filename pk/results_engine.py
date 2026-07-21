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
from pk.nca.lambda_z import calculate as calculate_lambda_z
from pk.nca.half_life import calculate as calculate_half_life
from app.models.analysis_result import AnalysisResult



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

        cmax_observation = calculate_cmax(
            observations
        )

        if cmax_observation is not None:
            result.cmax = cmax_observation.concentration
            result.tmax = calculate_tmax(
                cmax_observation
            )

        result.auc_0_t = calculate_auc(
            observations
        )

        lambda_result = calculate_lambda_z(
            observations
        )

        result.lambda_z = lambda_result.lambda_z
        result.t_half = calculate_half_life(
            lambda_result.lambda_z
        )

        result.terminal_points = (
            lambda_result.terminal_indices
        )

        result.terminal_r_squared = (
            lambda_result.r_squared
        )

        result.terminal_adjusted_r_squared = (
            lambda_result.adjusted_r_squared
        )

        result.terminal_sse = (
            lambda_result.sse
        )

        result.terminal_aic = (
            lambda_result.aic
        )

        result.terminal_bic = (
            lambda_result.bic
        )

        result.terminal_confidence = (
            lambda_result.confidence
        )

        return result