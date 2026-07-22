from app.models.observation import Observation


def calculate(
    observations: list[Observation],
) -> float | None:
    """
    Calculate AUMC from the first to last observation.
    """

    if len(observations) < 2:
        return None

    aumc = 0.0

    for left, right in zip(
        observations[:-1],
        observations[1:],
    ):
        delta_time = right.time - left.time

        if delta_time <= 0:
            raise ValueError(
                "Observation times must be strictly increasing."
            )

        left_moment = left.time * left.concentration
        right_moment = right.time * right.concentration

        aumc += (
            (left_moment + right_moment)
            / 2
            * delta_time
        )

    return aumc


def calculate_extrapolated(
    last_time: float | None,
    last_concentration: float | None,
    lambda_z: float | None,
) -> float | None:
    """
    Calculate the extrapolated portion of AUMC.
    """

    if (
        last_time is None
        or last_concentration is None
        or lambda_z is None
        or lambda_z <= 0
    ):
        return None

    return (
        last_time * last_concentration / lambda_z
        + last_concentration / lambda_z**2
    )


def calculate_infinity(
    aumc_0_t: float | None,
    aumc_extrapolated: float | None,
) -> float | None:
    """
    Calculate AUMC from zero to infinity.
    """

    if (
        aumc_0_t is None
        or aumc_extrapolated is None
    ):
        return None

    return aumc_0_t + aumc_extrapolated