import math


def calculate(
    lambda_z: float | None,
) -> float | None:
    """
    Calculate elimination half-life.
    """

    if lambda_z is None:
        return None

    if lambda_z <= 0:
        return None

    return math.log(2) / lambda_z