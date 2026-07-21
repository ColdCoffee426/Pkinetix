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
    method: AUCMethod = AUCMethod.LINEAR,
) -> float | None:
    """
    Calculate the area under the concentration-time curve
    from time zero to the last measurable concentration
    (AUC₀–t).
    """

    if len(observations) < 2:
        return None

    if method != AUCMethod.LINEAR:
        raise NotImplementedError(
            f"{method.value} method is not implemented yet."
        )

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

        trapezoid_area = (
            (
                left.concentration
                + right.concentration
            )
            / 2
        ) * delta_time

        auc += trapezoid_area

    return auc


def calculate_auc_infinity(
    auc_0_t: float | None,
    last_concentration: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate AUC from time zero to infinity.
    """

    if auc_0_t is None:
        return None

    if last_concentration is None:
        return None

    if lambda_z is None:
        return None

    if lambda_z <= 0:
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
    Calculate the extrapolated portion of AUC.
    """

    if auc_0_t is None:
        return None

    if auc_0_inf is None:
        return None

    return auc_0_inf - auc_0_t


def calculate_extrapolated_percent(
    auc_0_t: float | None,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate the percentage of extrapolated AUC.
    """

    extrapolated = calculate_extrapolated_auc(
        auc_0_t,
        auc_0_inf,
    )

    if extrapolated is None:
        return None

    if auc_0_inf is None:
        return None

    if auc_0_inf <= 0:
        return None

    return (
        extrapolated
        / auc_0_inf
        * 100
    )