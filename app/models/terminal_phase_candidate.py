from dataclasses import dataclass

from app.models.regression_result import RegressionResult


@dataclass(slots=True)
class TerminalPhaseCandidate:
    """
    Represents one possible terminal phase.
    """

    indices: list[int]
    times: list[float]
    concentrations: list[float]
    regression: RegressionResult | None = None