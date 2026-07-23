import math
from enum import Enum

from app.models.observation import Observation


class AUCMethod(Enum):
    """
    Supported AUC calculation methods.
    """

    LINEAR = "linear"
    LOG = "log"
    LINEAR_UP_LOG_DOWN = "linear_up_log_down"


def add_time_zero_observation(
    observations: list[Observation],
    concentration_at_zero: float = 0.0,
) -> list[Observation]:
    """
    Return a calculation-only copy containing a time-zero point.

    The project data and plotted observations are not modified.
    """

    if not observations:
        return []

    prepared = list(observations)
    first_time = prepared[0].time

    if first_time < 0:
        raise ValueError(
            "Observation times cannot be negative."
        )

    if first_time == 0:
        return prepared

    return [
        Observation(
            time=0.0,
            concentration=concentration_at_zero,
        ),
        *prepared,
    ]


def calculate(
    observations: list[Observation],
    method: AUCMethod = AUCMethod.LINEAR_UP_LOG_DOWN,
) -> float | None:
    """
    Calculate AUC over the supplied concentration-time observations.
    """

    if len(observations) < 2:
        return None

    if method == AUCMethod.LINEAR:
        return _linear_auc(observations)

    if method == AUCMethod.LOG:
        return _log_auc(observations)

    if method == AUCMethod.LINEAR_UP_LOG_DOWN:
        return _linear_up_log_down_auc(observations)

    raise NotImplementedError(
        f"{method.value} method is not implemented."
    )


def _validate_interval(
    left: Observation,
    right: Observation,
) -> float:
    delta_time = right.time - left.time

    if delta_time <= 0:
        raise ValueError(
            "Observation times must be strictly increasing."
        )

    return delta_time


def _linear_area(
    left: Observation,
    right: Observation,
) -> float:
    delta_time = _validate_interval(left, right)

    return (
        (left.concentration + right.concentration)
        / 2
        * delta_time
    )


def _log_area(
    left: Observation,
    right: Observation,
) -> float:
    delta_time = _validate_interval(left, right)
    c1 = left.concentration
    c2 = right.concentration

    if c1 <= 0 or c2 <= 0 or c1 == c2:
        return _linear_area(left, right)

    return (
        (c1 - c2)
        / math.log(c1 / c2)
        * delta_time
    )


def _linear_auc(
    observations: list[Observation],
) -> float:
    return sum(
        _linear_area(left, right)
        for left, right in zip(
            observations[:-1],
            observations[1:],
        )
    )


def _log_auc(
    observations: list[Observation],
) -> float:
    return sum(
        _log_area(left, right)
        for left, right in zip(
            observations[:-1],
            observations[1:],
        )
    )


def _linear_up_log_down_auc(
    observations: list[Observation],
) -> float:
    auc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        if right.concentration >= left.concentration:
            auc += _linear_area(left, right)
        else:
            auc += _log_area(left, right)

    return auc


def calculate_auc_infinity(
    auc_0_t: float | None,
    last_concentration: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate AUC from time zero to infinity.
    """

    if (
        auc_0_t is None
        or last_concentration is None
        or lambda_z is None
        or lambda_z <= 0
    ):
        return None

    return auc_0_t + last_concentration / lambda_z


def calculate_extrapolated_auc(
    auc_0_t: float | None,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate the extrapolated AUC portion.
    """

    if auc_0_t is None or auc_0_inf is None:
        return None

    return auc_0_inf - auc_0_t


def calculate_extrapolated_percent(
    auc_0_t: float | None,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate the percentage of AUC extrapolated to infinity.
    """

    if (
        auc_0_t is None
        or auc_0_inf is None
        or auc_0_inf <= 0
    ):
        return None

    return (
        (auc_0_inf - auc_0_t)
        / auc_0_inf
        * 100
    )
