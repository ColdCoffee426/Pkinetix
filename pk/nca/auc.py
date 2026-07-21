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

    Parameters
    ----------
    observations
        Validated concentration-time observations.
    method
        Numerical integration method.

    Returns
    -------
    float | None
        Calculated AUC₀–t or None if fewer than two
        observations are available.
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