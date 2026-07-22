import math

from app.models.lambda_z_result import LambdaZResult
from app.models.observation import Observation

from pk.common.goodness_of_fit import (
    bias,
    mae,
    rmse,
)
from pk.common.regression import linear_regression
from pk.common.statistics import regression_score
from pk.nca.terminal_phase import generate_candidates


MINIMUM_ADJUSTED_R2 = 0.80


def calculate(
    observations: list[Observation],
) -> LambdaZResult:
    """
    Estimate the terminal elimination rate constant (λz).
    """

    candidates = generate_candidates(
        observations
    )

    best_candidate = None
    best_regression = None

    for candidate in candidates:

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
        except Exception:
            continue

        if regression.slope >= 0:
            continue

        if (
            regression.adjusted_r_squared
            < MINIMUM_ADJUSTED_R2
        ):
            continue

        candidate.regression = regression

        candidate.score = regression_score(
            regression,
            len(candidate.indices),
        )

        if (
            best_candidate is None
            or candidate.score > best_candidate.score
        ):
            best_candidate = candidate
            best_regression = regression

    if (
        best_candidate is None
        or best_regression is None
    ):
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
            status="No valid terminal phase found",
        )

    confidence = min(
        100.0,
        max(
            0.0,
            best_candidate.score / 10,
        ),
    )

    fitted_times = list(
        best_candidate.times
    )

    fitted_concentrations = [
        math.exp(
            best_regression.intercept
            + best_regression.slope * time
        )
        for time in fitted_times
    ]

    fit_rmse = rmse(
        best_candidate.concentrations,
        fitted_concentrations,
    )

    fit_mae = mae(
        best_candidate.concentrations,
        fitted_concentrations,
    )

    fit_bias = bias(
        best_candidate.concentrations,
        fitted_concentrations,
    )

    return LambdaZResult(
        lambda_z=-best_regression.slope,
        slope=best_regression.slope,
        intercept=best_regression.intercept,
        r=best_regression.r,
        r_squared=best_regression.r_squared,
        adjusted_r_squared=(
            best_regression.adjusted_r_squared
        ),
        sse=best_regression.sse,
        aic=best_regression.aic,
        bic=best_regression.bic,
        terminal_indices=best_candidate.indices,
        terminal_times=best_candidate.times,
        terminal_concentrations=(
            best_candidate.concentrations
        ),
        confidence=confidence,
        status="Success",
        fitted_times=fitted_times,
        fitted_concentrations=fitted_concentrations,
        rmse=fit_rmse,
        mae=fit_mae,
        bias=fit_bias,
    )