from app.models.project import Project

from pk.analysis_engine import AnalysisEngine
from pk.results_engine import ResultsEngine


class AnalysisManager:
    """
    Coordinates all pharmacokinetic analyses.

    This is the main entry point into the PK engine.
    """

    def analyze(self, project: Project) -> dict:
        """
        Perform a complete analysis.
        """

        # Prepare analysis data
        engine = AnalysisEngine(project)

        analysis_project = engine.prepare()

        # Calculate results
        from pk.analysis_manager import AnalysisManager
        manager = AnalysisManager()

        results = manager.analyze(project)