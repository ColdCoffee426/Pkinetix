from dataclasses import dataclass


@dataclass
class ObservationInput:
    """
    Raw observation data entered by the user.

    This represents unvalidated table input.
    """

    row: int
    time: str
    concentration: str