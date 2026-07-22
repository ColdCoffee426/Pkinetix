from app.models.project import Project
from app.models.validation_result import ValidationResult


class DataValidator:
    """
    Validates pharmacokinetic input data.
    """

    def validate_value(
        self,
        time: str,
        concentration: str,
    ) -> ValidationResult:

        result = ValidationResult()

        if time.strip() == "":
            result.add_error(
                "Time cannot be empty."
            )

        if concentration.strip() == "":
            result.add_error(
                "Concentration cannot be empty."
            )

        if not result.is_valid:
            return result

        try:
            float(time)
        except ValueError:
            result.add_error(
                "Time must be numeric."
            )

        try:
            value = float(concentration)

            if value < 0:
                result.add_error(
                    "Concentration cannot be negative."
                )

        except ValueError:
            result.add_error(
                "Concentration must be numeric."
            )

        return result

    def validate(
        self,
        project: Project,
    ) -> ValidationResult:

        result = ValidationResult()

        observations = project.observations

        if len(observations) < 2:
            result.add_error(
                "At least two observations are required."
            )
            return result

        previous_time = None

        for index, observation in enumerate(observations):

            if observation.time is None:
                result.add_error(
                    f"Row {index+1}: Missing time."
                )

            if observation.concentration is None:
                result.add_error(
                    f"Row {index+1}: Missing concentration."
                )

            if (
                observation.concentration is not None
                and observation.concentration < 0
            ):
                result.add_error(
                    f"Row {index+1}: Negative concentration."
                )

            if previous_time is not None:

                if observation.time == previous_time:
                    result.add_error(
                        f"Row {index+1}: Duplicate time value."
                    )

                elif observation.time < previous_time:
                    result.add_error(
                        f"Row {index+1}: Time values must be increasing."
                    )

            previous_time = observation.time

        return result