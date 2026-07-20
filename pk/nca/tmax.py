from app.models.observation import Observation


def calculate(observation: Observation | None) -> float | None:
    """
    Return the time corresponding to Cmax.
    Parameters
    ----------
    observation
        Observation returned by the Cmax calculator.

    Returns
    -------
    float | None
        Time of maximum observed concentration.
    """
    if observation is None:
        return None

    return observation.time