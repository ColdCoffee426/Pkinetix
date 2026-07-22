from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    """
    Represents a single validation issue.
    """

    row: int | None
    field: str
    message: str