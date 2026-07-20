from app.models.project import Project
from app.services.data_validator import DataValidator
from app.models.observation import ObservationInput

from PySide6.QtCore import QObject, Signal




class ProjectController(QObject):
    """
    Controller responsible for coordinating
    GUI data and project model.
    """
    project_changed = Signal()

    def __init__(self, project: Project) -> None:
        self.project = project
        self.validator = DataValidator()
        self.validation_errors = []
        super().__init__()

    def update_observations(
        self,
        table_data: list[ObservationInput],
    ) -> None:
        """
        Update project observations from table data.
        """

        self.project.observations.clear()
        self.validation_errors.clear()

        for observation_input in table_data:

            result = self.validator.validate_value(
                observation_input.time,
                observation_input.concentration,
            )

            if not result.valid:
                self.validation_errors.append(
                    result
                )
                continue

            self.project.add_observation(
                float(observation_input.time),
                float(observation_input.concentration),
            )

            self.project_changed.emit()