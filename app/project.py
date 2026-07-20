from dataclasses import dataclass, field


@dataclass
class Project:
    """
    Represents an open PKinetix project.

    This class will eventually hold study information,
    concentration-time data, analysis results,
    application settings, and project metadata.
    """

    study_name: str = ""
    drug_name: str = ""
    subject_id: str = ""

    dose: float | None = None
    body_weight: float | None = None

    route: str = "Oral"

    comments: str = ""

    observations: list = field(default_factory=list)

    results: dict = field(default_factory=dict)