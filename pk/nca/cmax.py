from app.models.observation import Observation


def calculate(
    observations: list[Observation],
) -> Observation | None:
    """
    Calculate the maximum observed concentration.

    Parameters
    ----------
    observations
        Validated observations.

    Returns
    -------
    Observation | None
        Observation corresponding to Cmax.
    """

    if not observations:
        return None

    return max(
        observations,
        key=lambda observation: observation.concentration,
    )