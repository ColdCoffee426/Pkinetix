from dataclasses import dataclass


@dataclass(slots=True)
class ObservationInput:
    """
    Raw observation data entered by the user.

    This represents unvalidated table input.
    """

    row: int
    time: str
    concentration: str


@dataclass(slots=True)
class Observation:
    """
    Validated pharmacokinetic observation.

    This model is used throughout the PK engine after
    validation has converted the GUI input into numeric
    values.
    """

    time: float
    concentration: float