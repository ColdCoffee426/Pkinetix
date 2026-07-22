from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationResult:
    """
    Stores validation results.
    """

    is_valid: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )