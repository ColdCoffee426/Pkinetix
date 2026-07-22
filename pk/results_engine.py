"""
Coordinates pharmacokinetic result calculations.
"""

from app.models.analysis_result import AnalysisResult
from app.models.project import Project
from pk.nca.auc import AUCMethod
from pk.nca.cmax import calculate as calculate_cmax
from pk.nca.tmax import calculate as calculate_tmax
from pk.nca.auc import (
    calculate as calculate_auc,
    calculate_auc_infinity,
    calculate_extrapolated_auc,
    calculate_extrapolated_percent,
)
from pk.nca.lambda_z import calculate as calculate_lambda_z
from pk.nca.half_life import calculate as calculate_half_life
from pk.nca.aumc import calculate as calculate_aumc
from pk.nca.mrt import calculate as calculate_mrt
from pk.nca.clearance import calculate as calculate_clearance
from pk.nca.volume import calculate as calculate_volume


class ResultsEngine:

    def __init__(
        self,
        project: Project,
    ) -> None:
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
            observations,
            AUCMethod.LINEAR_UP_LOG_DOWN,
        )

        lambda_result = calculate_lambda_z(
            observations
        )

        result.lambda_z = lambda_result.lambda_z

        result.t_half = calculate_half_life(
            lambda_result.lambda_z
        )

        result.aumc = calculate_aumc(
            observations
        )

        result.mrt = calculate_mrt(
            result.auc_0_t,
            result.aumc,
        )

        last_concentration = (
            observations[-1].concentration
            if observations
            else None
        )

        result.auc_0_inf = calculate_auc_infinity(
            result.auc_0_t,
            last_concentration,
            result.lambda_z,
        )

        result.auc_extrapolated = (
            calculate_extrapolated_auc(
                result.auc_0_t,
                result.auc_0_inf,
            )
        )

        result.auc_extrapolated_percent = (
            calculate_extrapolated_percent(
                result.auc_0_t,
                result.auc_0_inf,
            )
        )

        result.cl = calculate_clearance(
            self.project,
            result.auc_0_inf,
        )

        result.vz = calculate_volume(
            result.cl,
            result.lambda_z,
        )

        result.terminal_points = (
            lambda_result.terminal_indices
        )

        result.terminal_times = (
            lambda_result.terminal_times
        )

        result.terminal_concentrations = (
            lambda_result.terminal_concentrations
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

        result.fitted_terminal_times = (
            lambda_result.fitted_times
        )

        result.fitted_terminal_concentrations = (
            lambda_result.fitted_concentrations
        )

        result.terminal_rmse = (
            lambda_result.rmse
        )

        result.terminal_mae = (
            lambda_result.mae
        )

        result.terminal_bias = (
            lambda_result.bias
        )

        return result