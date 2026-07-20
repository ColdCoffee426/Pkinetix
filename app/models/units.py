from dataclasses import dataclass

@dataclass(slots=True)
class Units:
    """
    Units used throughout a pharmacokinetic project.
    """
    time: str = "h"
    concentration: str = "ng/mL"
    dose: str = "mg"
    body_weight: str = "kg"