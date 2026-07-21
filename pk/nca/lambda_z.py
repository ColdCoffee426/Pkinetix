import math

from app.models.lambda_z_result import LambdaZResult
from pk.common.regression import linear_regression
from pk.nca.terminal_phase import generate_candidates
from app.models.observation import Observation

def calculate(
    observations: list[Observation],
) -> LambdaZResult:
    """
    Estimate the terminal elimination rate constant (λz).
    """

    candidates = generate_candidates(observations)

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

        regression = linear_regression(
            candidate.times,
            log_concentrations,
        )

        if regression.slope >= 0:
            continue

        candidate.regression = regression

        if (
            best_regression is None
            or regression.adjusted_r_squared
            > best_regression.adjusted_r_squared
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
        confidence=None,
        status="Success",
    )