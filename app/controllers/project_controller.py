from PySide6.QtCore import QObject, Signal

from app.models.observation import ObservationInput
from app.models.project import Project
from app.services.data_validator1 import DataValidator
from pk.analysis_manager import AnalysisManager


class ProjectController(QObject):
    """
    Coordinates GUI data, validation and explicit PK analysis.
    """

    project_changed = Signal()
    analysis_completed = Signal()

    def __init__(self, project: Project) -> None:
        super().__init__()
        self.project = project
        self.validator = DataValidator()
        self.analysis_manager = AnalysisManager()
        self.validation_errors = []
        self.project_validation = None
        self.analysis_result = None

    def update_observations(
        self,
        table_data: list[ObservationInput],
    ) -> None:
        """
        Update validated project observations without running analysis.
        """

        self.project.observations.clear()
        self.validation_errors.clear()

        for observation_input in table_data:
            result = self.validator.validate_value(
                observation_input.time,
                observation_input.concentration,
            )

            if not result.is_valid:
                self.validation_errors.append(result)
                continue

            self.project.add_observation(
                float(observation_input.time),
                float(observation_input.concentration),
            )

        self.project_validation = self.validator.validate(self.project)
        self.analysis_result = None
        self.project_changed.emit()

    def update_study_information(
        self,
        data: dict[str, str],
    ) -> None:
        """
        Update project metadata and units without running analysis.
        """

        self.project.study_name = data["study_name"]
        self.project.drug_name = data["drug_name"]
        self.project.subject_id = data["subject_id"]
        self.project.route = data["route"]
        self.project.auc_method = data["auc_method"]
        self.project.comments = data["comments"]

        self.project.units.dose = data["dose_unit"]
        self.project.units.concentration = data["concentration_unit"]
        self.project.units.time = data["time_unit"]
        self.project.units.body_weight = data["body_weight_unit"]
        self.project.units.clearance = f"L/{self.project.units.time}"
        self.project.units.auc = (
            f"{self.project.units.concentration}·{self.project.units.time}"
        )
        self.project.units.aumc = (
            f"{self.project.units.concentration}·{self.project.units.time}²"
        )

        self.project.dose = self._optional_positive_float(data["dose"])
        self.project.body_weight = self._optional_positive_float(
            data["body_weight"]
        )

        self.project_validation = self.validator.validate(self.project)
        self.analysis_result = None
        self.project_changed.emit()

    def analyze(self):
        """
        Validate the project and run PK calculations explicitly.
        """

        self.project_validation = self.validator.validate(self.project)

        if not self.project_validation.is_valid:
            self.analysis_result = None
            self.project_changed.emit()
            return None

        self.analysis_result = self.analysis_manager.analyze(self.project)
        self.analysis_completed.emit()
        self.project_changed.emit()
        return self.analysis_result

    def clear_analysis(self) -> None:
        self.analysis_result = None
        self.project_changed.emit()

    @staticmethod
    def _optional_positive_float(value: str) -> float | None:
        if value == "":
            return None

        try:
            numeric_value = float(value)
        except ValueError:
            return None

        if numeric_value <= 0:
            return None

        return numeric_value
