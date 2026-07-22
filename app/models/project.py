from dataclasses import dataclass, field


@dataclass(slots=True)
class Units:

    time: str = "h"
    concentration: str = "ng/mL"
    dose: str = "mg"
    body_weight: str = "kg"
    volume: str = "L"
    clearance: str = "L/h"
    auc: str = "ng·h/mL"
    aumc: str = "ng·h²/mL"
    auc_method: str = "linear_up_log_down"

@dataclass(slots=True)
class Observation:
    """
    Clean concentration-time observation.
    """

    time: float | None = None
    concentration: float | None = None


@dataclass(slots=True)
class Project:
    """
    Represents a PKinetix project.
    """

    study_name: str = ""
    drug_name: str = ""
    subject_id: str = ""

    dose: float | None = None
    body_weight: float | None = None

    comments: str = ""

    route: str | None = None

    units: Units = field(
        default_factory=Units
    )

    observations: list[Observation] = field(
        default_factory=list
    )


    def add_observation(
        self,
        time: float,
        concentration: float,
    ) -> None:
        """
        Add cleaned observation data.
        """

        self.observations.append(
            Observation(
                time=time,
                concentration=concentration,
            )
        )