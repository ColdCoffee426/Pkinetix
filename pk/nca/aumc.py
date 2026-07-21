from app.models.observation import Observation


def calculate(
    observations: list[Observation],
) -> float | None:
    """
    Calculate AUMC from time zero to the last observation.
    """

    if len(observations) < 2:
        return None

    aumc = 0.0

    for current, next_observation in zip(
        observations[:-1],
        observations[1:],
    ):
        dt = (
            next_observation.time
            - current.time
        )

        term1 = (
            current.time
            * current.concentration
        )

        term2 = (
            next_observation.time
            * next_observation.concentration
        )

        aumc += (
            (term1 + term2)
            / 2
        ) * dt

    return aumc