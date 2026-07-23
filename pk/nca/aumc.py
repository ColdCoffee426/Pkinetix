import math

from app.models.observation import Observation
from pk.nca.auc import AUCMethod


def calculate(
    observations: list[Observation],
    method: AUCMethod = AUCMethod.LINEAR_UP_LOG_DOWN,
) -> float | None:
    """
    Calculate AUMC over the supplied observations.
    """

    if len(observations) < 2:
        return None

    aumc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = right.time - left.time

        if delta_time <= 0:
            raise ValueError(
                "Observation times must be strictly increasing."
            )

        use_log = (
            method == AUCMethod.LOG
            or (
                method == AUCMethod.LINEAR_UP_LOG_DOWN
                and right.concentration < left.concentration
            )
        )

        if use_log:
            area = _log_moment_area(
                left,
                right,
                delta_time,
            )
        else:
            area = _linear_moment_area(
                left,
                right,
                delta_time,
            )

        aumc += area

    return aumc


def _linear_moment_area(
    left: Observation,
    right: Observation,
    delta_time: float,
) -> float:
    left_moment = left.time * left.concentration
    right_moment = right.time * right.concentration

    return (
        (left_moment + right_moment)
        / 2
        * delta_time
    )


def _log_moment_area(
    left: Observation,
    right: Observation,
    delta_time: float,
) -> float:
    c1 = left.concentration
    c2 = right.concentration

    if c1 <= 0 or c2 <= 0 or c1 == c2:
        return _linear_moment_area(
            left,
            right,
            delta_time,
        )

    log_ratio = math.log(c1 / c2)

    return (
        delta_time
        * (left.time * c1 - right.time * c2)
        / log_ratio
        + delta_time**2
        * (c1 - c2)
        / log_ratio**2
    )


def calculate_extrapolated(
    last_time: float | None,
    last_concentration: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate the extrapolated portion of AUMC.
    """

    if (
        last_time is None
        or last_concentration is None
        or lambda_z is None
        or lambda_z <= 0
    ):
        return None

    return (
        last_time * last_concentration / lambda_z
        + last_concentration / lambda_z**2
    )


def calculate_infinity(
    aumc_0_t: float | None,
    aumc_extrapolated: float | None,
) -> float | None:
    """
    Calculate AUMC from time zero to infinity.
    """

    if (
        aumc_0_t is None
        or aumc_extrapolated is None
    ):
        return None

    return aumc_0_t + aumc_extrapolated
