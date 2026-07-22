from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationResult:
    """
    Stores validation results.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(
        self,
        message: str,
    ) -> None:
        self.errors.append(message)

    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(message)