from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    """
    Represents a single validation problem.
    """

    row: int
    column: int
    message: str