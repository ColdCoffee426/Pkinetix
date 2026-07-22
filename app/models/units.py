from dataclasses import dataclass


@dataclass(slots=True)
class Units:
    """
    Stores measurement units used by a project.
    """

    time: str = "h"
    concentration: str = "ng/mL"
    dose: str = "mg"
    body_weight: str = "kg"
    volume: str = "L"
    clearance: str = "L/h"
    auc: str = "ng·h/mL"
    aumc: str = "ng·h²/mL"