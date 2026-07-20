from dataclasses import dataclass, field
@dataclass
class Observation:
    """
    Single concentration-time observation.
    """
    time: float | None = None
    concentration: float | None = None

@dataclass
class Project:
    """
    Represents a PKinetix project.
    Stores study information and experimental data.
    """
    study_name: str = ""
    drug_name: str = ""
    subject_id: str = ""
    dose: float | None = None
    body_weight: float | None = None
    comments: str = ""
    route: str | None = None
    observations: list[Observation] = field(
        default_factory=list
    )

    def add_observation(
        self,
        time: float,
        concentration: float,
    ) -> None:
        """
        Add a concentration-time observation.
        """

        self.observations.append(
            Observation(
                time=time,
                concentration=concentration,
            )
        )