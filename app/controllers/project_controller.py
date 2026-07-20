from app.models.project import Project
from app.services.data_validator import DataValidator


class ProjectController:
    """
    Controller responsible for coordinating
    GUI data and project model.
    """

    def __init__(self, project: Project) -> None:
        self.project = project
        self.validator = DataValidator()

    def update_observations(
        self,
        table_data: list[tuple[str, str]],
    ) -> None:
        """
        Update project observations from table data.
        """

        self.project.observations.clear()

        for time, concentration in table_data:

            if not time or not concentration:
                continue

            result = self.validator.validate_value(
            time,
            concentration,
        )

            if not result.valid:
                continue


            observation = (
                float(time),
                float(concentration),
            )
            
            self.project.add_observation(
                observation[0],
                observation[1],
            )