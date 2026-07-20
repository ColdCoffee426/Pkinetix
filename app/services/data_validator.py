from dataclasses import dataclass

@dataclass
class ValidationResult:
    """
    Result returned after validation.
    """
    valid: bool
    message: str = ""

class DataValidator:
    """
    Validates pharmacokinetic concentration-time data.
    """
    def validate_value(
        self,
        time: str,
        concentration: str,
    ) -> ValidationResult:
        """
        Validate a single observation.
        """

        if not time or not concentration:
            return ValidationResult(
                False,
                "Missing value"
            )

        try:
            time_value = float(time)
            concentration_value = float(concentration)

        except ValueError:
            return ValidationResult(
                False,
                "Values must be numeric"
            )

        if time_value < 0:
            return ValidationResult(
                False,
                "Time cannot be negative"
            )

        if concentration_value < 0:
            return ValidationResult(
                False,
                "Concentration cannot be negative"
            )

        return ValidationResult(True)