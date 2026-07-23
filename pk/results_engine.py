"""
Coordinates pharmacokinetic result calculations.
"""

from app.models.analysis_result import AnalysisResult
from app.models.project import Project
from pk.nca.auc import (
    AUCMethod,
    add_time_zero_observation,
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
        auc_method = self._get_auc_method()
        integration_observations = (
            self._get_integration_observations(result)
        )

        cmax_observation = calculate_cmax(observations)

        if cmax_observation is not None:
            result.cmax = cmax_observation.concentration
            result.tmax = calculate_tmax(cmax_observation)

        result.auc_0_t = calculate_auc(
            integration_observations,
            auc_method,
        )

        lambda_result = calculate_lambda_z(observations)
        result.lambda_z = lambda_result.lambda_z
        result.t_half = calculate_half_life(
            lambda_result.lambda_z
        )

        result.aumc = calculate_aumc(
            integration_observations,
            auc_method,
        )

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

        self._copy_terminal_results(
            result,
            lambda_result,
        )

        if result.lambda_z is None:
            result.warnings.append(
                "AUC 0-inf could not be calculated because "
                "a valid terminal elimination phase was not found."
            )
        elif (
            lambda_result.adjusted_r_squared is not None
            and lambda_result.adjusted_r_squared < 0.90
        ):
            result.warnings.append(
                "The terminal phase fit is weak; AUC 0-inf "
                "and half-life should be interpreted cautiously."
            )

        if (
            result.auc_extrapolated_percent is not None
            and result.auc_extrapolated_percent > 20
        ):
            result.warnings.append(
                "More than 20% of AUC 0-inf is extrapolated."
            )

        result.route = self.project.route
        return result

    def _get_integration_observations(
        self,
        result: AnalysisResult,
    ):
        observations = self.project.observations

        if not observations:
            return []

        if observations[0].time == 0:
            return list(observations)

        if self.project.route == "IV Bolus":
            result.warnings.append(
                "No time-zero concentration was entered. "
                "IV bolus back-extrapolation to C0 is not yet "
                "implemented, so AUC begins at the first sample."
            )
            return list(observations)

        result.notes.append(
            "A calculation-only concentration of zero was "
            "imputed at time zero for AUC and AUMC."
        )

        return add_time_zero_observation(observations)

    @staticmethod
    def _copy_terminal_results(
        result: AnalysisResult,
        lambda_result,
    ) -> None:
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

    def _get_auc_method(self) -> AUCMethod:
        try:
            return AUCMethod(self.project.auc_method)
        except ValueError:
            return AUCMethod.LINEAR_UP_LOG_DOWN
