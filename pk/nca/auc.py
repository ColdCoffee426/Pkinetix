from enum import Enum

from app.models.observation import Observation


class AUCMethod(Enum):
    LINEAR = "linear"

def calculate(
    observations: list[Observation],
    method: AUCMethod = AUCMethod.LINEAR,
) -> float | None:
    """
    Calculate AUC from time zero to the last observation.
    """

    if len(observations) < 2:
        return None

    if method != AUCMethod.LINEAR:
        raise NotImplementedError(
            f"{method.value} is not implemented yet."
        )

    auc = 0.0

    for current, next_observation in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = (
            next_observation.time
            - current.time
        )

        trapezoid = (
            current.concentration
            + next_observation.concentration
        ) / 2

        auc += trapezoid * delta_time

    return auc