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
        """
        Validate individual table entry.
        """

        result = ValidationResult()

        if time.strip() == "":
            result.is_valid = False
            result.errors.append(
                "Time cannot be empty."
            )

        if concentration.strip() == "":
            result.is_valid = False
            result.errors.append(
                "Concentration cannot be empty."
            )

        if not result.is_valid:
            return result

        try:
            float(time)
        except ValueError:
            result.is_valid = False
            result.errors.append(
                "Time must be a number."
            )

        try:
            value = float(concentration)

            if value < 0:
                result.is_valid = False
                result.errors.append(
                    "Concentration cannot be negative."
                )

        except ValueError:
            result.is_valid = False
            result.errors.append(
                "Concentration must be a number."
            )

        return result


    def validate(
        self,
        project: Project,
    ) -> ValidationResult:
        """
        Validate complete project data.
        """

        result = ValidationResult()

        if len(project.observations) < 2:
            result.is_valid = False

            result.errors.append(
                "At least two observations are required."
            )

            return result


        previous_time = None

        for index, observation in enumerate(
            project.observations
        ):

            if observation.time is None:
                result.is_valid = False

                result.errors.append(
                    f"Row {index + 1}: Missing time."
                )

            if observation.concentration is None:
                result.is_valid = False

                result.errors.append(
                    f"Row {index + 1}: Missing concentration."
                )


            if observation.concentration is not None:

                if observation.concentration < 0:
                    result.is_valid = False

                    result.errors.append(
                        f"Row {index + 1}: Negative concentration."
                    )


            if previous_time is not None:

                if observation.time <= previous_time:
                    result.warnings.append(
                        f"Row {index + 1}: Time values are not increasing."
                    )


            previous_time = observation.time


        return result