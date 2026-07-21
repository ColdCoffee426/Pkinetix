def calculate(
    clearance: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate apparent volume of distribution.
    """

    if clearance is None:
        return None

    if lambda_z is None:
        return None

    if lambda_z <= 0:
        return None

    return clearance / lambda_z