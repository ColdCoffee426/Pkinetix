from dataclasses import dataclass


@dataclass(slots=True)
class TerminalPhaseCandidate:
    """
    Represents one possible terminal phase.
    """

    indices: list[int]
    times: list[float]
    concentrations: list[float]