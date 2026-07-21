from dataclasses import dataclass


@dataclass(slots=True)
class RegressionResult:
    """
    Stores the results of a simple linear regression.
    """

    slope: float
    intercept: float

    r: float
    r_squared: float
    adjusted_r_squared: float

    sse: float

    aic: float
    bic: float