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
        Validate a single table row.
        """

        result = ValidationResult()

        if time.strip() == "":
            result.add_issue(
                0,
                0,
                "Time cannot be empty.",
            )

        if concentration.strip() == "":
            result.add_issue(
                0,
                1,
                "Concentration cannot be empty.",
            )

        if not result.is_valid:
            return result

        try:
            float(time)
        except ValueError:
            result.add_issue(
                0,
                0,
                "Time must be numeric.",
            )

        try:
            value = float(concentration)

            if value < 0:
                result.add_issue(
                    0,
                    1,
                    "Concentration cannot be negative.",
                )

        except ValueError:
            result.add_issue(
                0,
                1,
                "Concentration must be numeric.",
            )

        return result

    def validate(
        self,
        project: Project,
    ) -> ValidationResult:
        """
        Validate the complete project.
        """

        result = ValidationResult()

        observations = project.observations

        if len(observations) < 2:
            result.add_issue(
                0,
                0,
                "At least two observations are required.",
            )
            return result

        previous_time = None

        for index, observation in enumerate(observations):

            if observation.time is None:
                result.add_issue(
                    index,
                    0,
                    "Missing time.",
                )

            if observation.concentration is None:
                result.add_issue(
                    index,
                    1,
                    "Missing concentration.",
                )

            if (
                observation.concentration is not None
                and observation.concentration < 0
            ):
                result.add_issue(
                    index,
                    1,
                    "Negative concentration.",
                )

            if previous_time is not None:

                if observation.time == previous_time:
                    result.add_issue(
                        index,
                        0,
                        "Duplicate time value.",
                    )

                elif observation.time < previous_time:
                    result.add_issue(
                        index,
                        0,
                        "Time values must be increasing.",
                    )

            previous_time = observation.time

        return result