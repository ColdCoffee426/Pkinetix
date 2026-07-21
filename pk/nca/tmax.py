from app.models.observation import Observation


def calculate(
    cmax_observation: Observation | None,
) -> float | None:
    """
    Calculate the time corresponding to the maximum observed
    concentration (Tmax).

    Parameters
    ----------
    cmax_observation
        Observation returned by the Cmax calculator.

    Returns
    -------
    float | None
        Time of maximum observed concentration.
    """

    if cmax_observation is None:
        return None

    return cmax_observation.time