from app.models.project import Project

from pk.analysis_engine import AnalysisEngine
from pk.results_engine import ResultsEngine


class AnalysisManager:
    """
    Coordinates all pharmacokinetic analyses.

    This is the main entry point into the PK engine.
    """

    def analyze(self, project: Project):
        """
        Perform a complete pharmacokinetic analysis.
        """

        engine = AnalysisEngine(project)
        prepared_project = engine.prepare()

        results = ResultsEngine(
            prepared_project
        ).calculate()

        return results