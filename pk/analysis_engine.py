##this file will be prepare the data and is not for calculations, basically a data prep layer.

from app.models.project import Project
class AnalysisEngine:
    """
    Coordinates pharmacokinetic analyses.

    At this stage, it only prepares validated
    concentration-time data for visualization.

    Future responsibilities:
    - Non-compartmental analysis
    - Compartmental analysis
    - Statistics
    - Simulation
    """

    def __init__(self, project: Project) -> None:
        self.project = project

    def get_plot_data(self) -> tuple[list[float], list[float]]:
        """
        Return time and concentration values for plotting.
        """

        observations = sorted(
            self.project.observations,
            key=lambda observation: observation.time,
        )

        time = [
            observation.time
            for observation in observations
        ]

        concentration = [
            observation.concentration
            for observation in observations
        ]

        return time, concentration