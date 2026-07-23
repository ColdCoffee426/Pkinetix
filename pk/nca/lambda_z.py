import math

from app.models.lambda_z_result import LambdaZResult
from app.models.observation import Observation
from pk.common.goodness_of_fit import bias, mae, rmse
from pk.common.regression import linear_regression
from pk.nca.terminal_phase import generate_candidates


ADJUSTED_R2_TOLERANCE = 1e-4
GOOD_FIT_ADJUSTED_R2 = 0.90


def calculate(
    observations: list[Observation],
) -> LambdaZResult:
    """
    Estimate the terminal elimination rate constant.
    """

    valid_fits = []

    for candidate in generate_candidates(observations):
        if any(
            concentration <= 0
            for concentration in candidate.concentrations
        ):
            continue

        log_concentrations = [
            math.log(concentration)
            for concentration in candidate.concentrations
        ]

        try:
            regression = linear_regression(
                candidate.times,
                log_concentrations,
            )
        except (ValueError, ArithmeticError):
            continue

        if regression.slope >= 0:
            continue

        candidate.regression = regression
        valid_fits.append((candidate, regression))

    if not valid_fits:
        return _empty_result(
            "No valid terminal phase found"
        )

    best_adjusted_r2 = max(
        regression.adjusted_r_squared
        for _, regression in valid_fits
    )

    eligible_fits = [
        (candidate, regression)
        for candidate, regression in valid_fits
        if regression.adjusted_r_squared
        >= best_adjusted_r2 - ADJUSTED_R2_TOLERANCE
    ]

    best_candidate, best_regression = max(
        eligible_fits,
        key=lambda fit: len(fit[0].indices),
    )

    fitted_times = list(best_candidate.times)
    fitted_concentrations = [
        math.exp(
            best_regression.intercept
            + best_regression.slope * time
        )
        for time in fitted_times
    ]

    adjusted_r2 = best_regression.adjusted_r_squared
    confidence = max(
        0.0,
        min(100.0, adjusted_r2 * 100),
    )

    status = (
        "Good fit"
        if adjusted_r2 >= GOOD_FIT_ADJUSTED_R2
        else "Poor fit"
    )

    return LambdaZResult(
        lambda_z=-best_regression.slope,
        slope=best_regression.slope,
        intercept=best_regression.intercept,
        r=best_regression.r,
        r_squared=best_regression.r_squared,
        adjusted_r_squared=adjusted_r2,
        sse=best_regression.sse,
        aic=best_regression.aic,
        bic=best_regression.bic,
        terminal_indices=best_candidate.indices,
        terminal_times=best_candidate.times,
        terminal_concentrations=(
            best_candidate.concentrations
        ),
        confidence=confidence,
        status=status,
        fitted_times=fitted_times,
        fitted_concentrations=fitted_concentrations,
        rmse=rmse(
            best_candidate.concentrations,
            fitted_concentrations,
        ),
        mae=mae(
            best_candidate.concentrations,
            fitted_concentrations,
        ),
        bias=bias(
            best_candidate.concentrations,
            fitted_concentrations,
        ),
    )


def _empty_result(status: str) -> LambdaZResult:
    return LambdaZResult(
        lambda_z=None,
        slope=None,
        intercept=None,
        r=None,
        r_squared=None,
        adjusted_r_squared=None,
        sse=None,
        aic=None,
        bic=None,
        terminal_indices=[],
        terminal_times=[],
        terminal_concentrations=[],
        confidence=None,
        status=status,
    )
