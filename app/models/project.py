from dataclasses import dataclass, field

from app.models.observation import Observation
from app.models.units import Units


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
    auc_method: str = "linear_up_log_down"

    units: Units = field(default_factory=Units)
    observations: list[Observation] = field(default_factory=list)

    def add_observation(
        self,
        time: float,
        concentration: float,
    ) -> None:
        """
        Add validated observation data.
        """

        self.observations.append(
            Observation(
                time=time,
                concentration=concentration,
            )
        )