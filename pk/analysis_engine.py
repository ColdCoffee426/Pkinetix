from app.models.project import Project


class AnalysisEngine:
    """
    Prepares project data before analysis.
    """

    def __init__(self, project: Project):
        self.project = project

    def prepare(self) -> Project:
        """
        Prepare analysis data.

        Future responsibilities:

        - Remove empty rows
        - Validate observations
        - Unit conversion
        - Sort observations
        """

        return self.project