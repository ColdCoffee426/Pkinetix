from app.models.observation import Observation
from app.models.terminal_phase_candidate import (
    TerminalPhaseCandidate,
)


def generate_candidates(
    observations: list[Observation],
    minimum_points: int = 3,
) -> list[TerminalPhaseCandidate]:
    """
    Generate all possible terminal phase candidates.

    Each candidate contains the final observations of the
    concentration-time profile.

    Parameters
    ----------
    observations
        Validated observations.

    minimum_points
        Minimum number of observations required for a
        terminal phase.

    Returns
    -------
    list[TerminalPhaseCandidate]
    """

    candidates: list[
        TerminalPhaseCandidate
    ] = []

    observation_count = len(observations)

    if observation_count < minimum_points:
        return candidates

    for start in range(
        observation_count - minimum_points,
        -1,
        -1,
    ):
        subset = observations[start:]

        candidate = TerminalPhaseCandidate(
            indices=list(
                range(
                    start,
                    observation_count,
                )
            ),
            times=[
                observation.time
                for observation in subset
            ],
            concentrations=[
                observation.concentration
                for observation in subset
            ],
        )

        candidates.append(candidate)

    return candidates