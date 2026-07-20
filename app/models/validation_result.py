from dataclasses import dataclass, field

from app.models.validation_issue import ValidationIssue


@dataclass(slots=True)
class ValidationResult:
    """
    Stores all validation issues.
    """

    issues: list[ValidationIssue] = field(
        default_factory=list
    )

    @property
    def is_valid(self) -> bool:
        return len(self.issues) == 0

    def add_issue(
        self,
        row: int,
        column: int,
        message: str,
    ) -> None:

        self.issues.append(
            ValidationIssue(
                row=row,
                column=column,
                message=message,
            )
        )