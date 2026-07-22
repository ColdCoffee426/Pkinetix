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


def calculate(
    observations: list[Observation],
    method: AUCMethod = AUCMethod.LINEAR_UP_LOG_DOWN,
) -> float | None:
    """
    Calculate AUC from time zero to the last observation.
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


def _linear_auc(
    observations: list[Observation],
) -> float:

    auc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = right.time - left.time

        if delta_time <= 0:
            raise ValueError(
                "Observation times must be strictly increasing."
            )

        auc += (
            (
                left.concentration
                + right.concentration
            )
            / 2
        ) * delta_time

    return auc


def _log_auc(
    observations: list[Observation],
) -> float:

    auc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = right.time - left.time

        if delta_time <= 0:
            raise ValueError(
                "Observation times must be strictly increasing."
            )

        c1 = left.concentration
        c2 = right.concentration

        if (
            c1 <= 0
            or c2 <= 0
            or c1 == c2
        ):
            area = (
                (c1 + c2)
                / 2
            ) * delta_time

        else:
            area = (
                (c1 - c2)
                / math.log(c1 / c2)
            ) * delta_time

        auc += area

    return auc


def _linear_up_log_down_auc(
    observations: list[Observation],
) -> float:

    auc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = right.time - left.time

        if delta_time <= 0:
            raise ValueError(
                "Observation times must be strictly increasing."
            )

        c1 = left.concentration
        c2 = right.concentration

        if c2 >= c1:

            area = (
                (c1 + c2)
                / 2
            ) * delta_time

        else:

            if (
                c1 <= 0
                or c2 <= 0
                or c1 == c2
            ):
                area = (
                    (c1 + c2)
                    / 2
                ) * delta_time

            else:
                area = (
                    (c1 - c2)
                    / math.log(c1 / c2)
                ) * delta_time

        auc += area

    return auc


def calculate_auc_infinity(
    auc_0_t: float | None,
    last_concentration: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate AUC₀-∞.
    """

    if (
        auc_0_t is None
        or last_concentration is None
        or lambda_z is None
        or lambda_z <= 0
    ):
        return None

    return (
        auc_0_t
        + last_concentration / lambda_z
    )


def calculate_extrapolated_auc(
    auc_0_t: float | None,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate extrapolated AUC.
    """

    if (
        auc_0_t is None
        or auc_0_inf is None
    ):
        return None

    return auc_0_inf - auc_0_t


def calculate_extrapolated_percent(
    auc_0_t: float | None,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate percent extrapolated AUC.
    """

    if (
        auc_0_t is None
        or auc_0_inf is None
        or auc_0_inf == 0
    ):
        return None

    return (
        (auc_0_inf - auc_0_t)
        / auc_0_inf
    ) * 100