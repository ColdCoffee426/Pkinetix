from app.models.project import Project


class ResultsEngine:
    """
    Coordinates pharmacokinetic result calculations.

    Individual PK parameters are delegated to dedicated
    calculator modules.
    """

    def __init__(self, project: Project) -> None:
        self.project = project

    def calculate(self) -> dict[str, float | None]:
        """
        Return all calculated PK parameters.

        Currently returns placeholders.
        """

        return {
            "Cmax": None,
            "Tmax": None,
            "Lambda_z": None,
            "Half-life": None,
            "AUC0-t": None,
            "AUC0-inf": None,
            "AUMC": None,
            "MRT": None,
            "Clearance": None,
            "Vz": None,
        }