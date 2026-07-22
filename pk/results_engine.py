"""
Coordinates pharmacokinetic result calculations.
"""

from app.models.analysis_result import AnalysisResult
from app.models.project import Project
from pk.nca.auc import (
    AUCMethod,
    calculate as calculate_auc,
    calculate_auc_infinity,
    calculate_extrapolated_auc,
    calculate_extrapolated_percent,
)
from pk.nca.aumc import (
    calculate as calculate_aumc,
    calculate_extrapolated as calculate_aumc_extrapolated,
    calculate_infinity as calculate_aumc_infinity,
)
from pk.nca.clearance import calculate as calculate_clearance
from pk.nca.cmax import calculate as calculate_cmax
from pk.nca.half_life import calculate as calculate_half_life
from pk.nca.lambda_z import calculate as calculate_lambda_z
from pk.nca.mrt import calculate as calculate_mrt
from pk.nca.tmax import calculate as calculate_tmax
from pk.nca.volume import calculate as calculate_volume


class ResultsEngine:
    """
    Coordinates pharmacokinetic result calculations.
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

        result.auc_0_t = calculate_auc(
            observations,
            self._get_auc_method(),
        )

        lambda_result = calculate_lambda_z(observations)

        result.lambda_z = lambda_result.lambda_z
        result.t_half = calculate_half_life(
            lambda_result.lambda_z
        )

        result.aumc = calculate_aumc(observations)

        last_time = (
            observations[-1].time
            if observations
            else None
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

        result.aumc_extrapolated = (
            calculate_aumc_extrapolated(
                last_time,
                last_concentration,
                result.lambda_z,
            )
        )
        result.aumc_0_inf = calculate_aumc_infinity(
            result.aumc,
            result.aumc_extrapolated,
        )
        result.mrt = calculate_mrt(
            result.auc_0_inf,
            result.aumc_0_inf,
        )

        result.cl = calculate_clearance(
            self.project,
            result.auc_0_inf,
        )
        result.vz = calculate_volume(
            result.cl,
            result.lambda_z,
        )

        if (
            result.vz is not None
            and self.project.body_weight is not None
            and self.project.body_weight > 0
        ):
            result.vd_per_kg = (
                result.vz / self.project.body_weight
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
        result.terminal_r_squared = lambda_result.r_squared
        result.terminal_adjusted_r_squared = (
            lambda_result.adjusted_r_squared
        )
        result.terminal_sse = lambda_result.sse
        result.terminal_aic = lambda_result.aic
        result.terminal_bic = lambda_result.bic
        result.terminal_confidence = (
            lambda_result.confidence
        )
        result.terminal_rmse = lambda_result.rmse
        result.terminal_mae = lambda_result.mae
        result.terminal_bias = lambda_result.bias

        result.fitted_terminal_times = (
            lambda_result.fitted_times
        )
        result.fitted_terminal_concentrations = (
            lambda_result.fitted_concentrations
        )

        result.route = self.project.route

        return result

    def _get_auc_method(self) -> AUCMethod:
        try:
            return AUCMethod(self.project.auc_method)
        except ValueError:
            return AUCMethod.LINEAR_UP_LOG_DOWN