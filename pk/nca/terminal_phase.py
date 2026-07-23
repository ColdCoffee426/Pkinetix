from app.models.observation import Observation
from app.models.terminal_phase_candidate import (
    TerminalPhaseCandidate,
)


def generate_candidates(
    observations: list[Observation],
    minimum_points: int = 3,
    allow_tmax: bool = True,
) -> list[TerminalPhaseCandidate]:
    """
    Generate terminal-phase candidates ending at the last point.

    Pre-Tmax observations are excluded. Tmax may be included when
    allow_tmax is True.
    """

    if len(observations) < minimum_points:
        return []

    cmax_index = max(
        range(len(observations)),
        key=lambda index: observations[index].concentration,
    )

    earliest_start = (
        cmax_index
        if allow_tmax
        else cmax_index + 1
    )

    latest_start = len(observations) - minimum_points

    if earliest_start > latest_start:
        return []

    candidates: list[TerminalPhaseCandidate] = []

    for start in range(
        latest_start,
        earliest_start - 1,
        -1,
    ):
        subset = observations[start:]

        candidates.append(
            TerminalPhaseCandidate(
                indices=list(
                    range(start, len(observations))
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
        )

    return candidates
