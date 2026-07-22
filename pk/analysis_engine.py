from app.models.project import Project


class AnalysisEngine:
    """
    Prepares project data before analysis.
    """

    def __init__(
        self,
        project: Project,
    ) -> None:
        self.project = project

    def prepare(self) -> Project:
        """
        Prepare project before PK analysis.
        """

        self._sort_observations()

        return self.project

    def _sort_observations(self) -> None:
        """
        Ensure observations are sorted by time.
        """

        self.project.observations.sort(
            key=lambda observation: observation.time
        )

    def get_plot_data(
        self,
    ) -> tuple[list[float], list[float]]:
        """
        Return plotting data.
        """

        time = [
            observation.time
            for observation in self.project.observations
        ]

        concentration = [
            observation.concentration
            for observation in self.project.observations
        ]

        return time, concentration