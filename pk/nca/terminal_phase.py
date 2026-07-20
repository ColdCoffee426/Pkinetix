from app.models.project import Project
from app.models.terminal_phase_candidate import TerminalPhaseCandidate


MIN_TERMINAL_POINTS = 3


def generate_terminal_candidates(
    project: Project,
) -> list[TerminalPhaseCandidate]:
    """
    Generate all possible terminal phase candidates.
    """

    observations = project.observations

    candidates: list[TerminalPhaseCandidate] = []

    for start in range(
        len(observations) - MIN_TERMINAL_POINTS
    ):
        subset = observations[start:]

        if len(subset) < MIN_TERMINAL_POINTS:
            continue

        candidates.append(
            TerminalPhaseCandidate(
                indices=list(range(start, len(observations))),
                times=[o.time for o in subset],
                concentrations=[o.concentration for o in subset],
            )
        )

    return candidates