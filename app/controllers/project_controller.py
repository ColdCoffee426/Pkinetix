from PySide6.QtCore import QObject, Signal

from app.models.observation import ObservationInput
from app.models.project import Project
from app.services.data_validator import DataValidator
from pk.analysis_manager import AnalysisManager


class ProjectController(QObject):
    """
    Coordinates GUI data, validation and PK analysis.
    """

    project_changed = Signal()

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

        self._refresh_analysis()

    def update_study_information(
        self,
        data: dict[str, str],
    ) -> None:
        self.project.study_name = data["study_name"]
        self.project.drug_name = data["drug_name"]
        self.project.subject_id = data["subject_id"]
        self.project.route = data["route"]
        self.project.auc_method = data["auc_method"]
        self.project.comments = data["comments"]

        self.project.units.dose = data["dose_unit"]
        self.project.units.concentration = (
            data["concentration_unit"]
        )
        self.project.units.time = data["time_unit"]
        self.project.units.body_weight = (
            data["body_weight_unit"]
        )

        self.project.units.clearance = (
            f"L/{self.project.units.time}"
        )
        self.project.units.auc = (
            f"{self.project.units.concentration}"
            f"·{self.project.units.time}"
        )
        self.project.units.aumc = (
            f"{self.project.units.concentration}"
            f"·{self.project.units.time}²"
        )

        self.project.dose = self._optional_positive_float(
            data["dose"]
        )
        self.project.body_weight = self._optional_positive_float(
            data["body_weight"]
        )

        self._refresh_analysis()

    def _refresh_analysis(self) -> None:
        self.project_validation = self.validator.validate(
            self.project
        )

        if self.project_validation.is_valid:
            self.analysis_result = self.analysis_manager.analyze(
                self.project
            )
        else:
            self.analysis_result = None

        self.project_changed.emit()

    @staticmethod
    def _optional_positive_float(
        value: str,
    ) -> float | None:
        if value == "":
            return None

        try:
            numeric_value = float(value)
        except ValueError:
            return None

        if numeric_value <= 0:
            return None

        return numeric_value