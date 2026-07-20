from dataclasses import dataclass


@dataclass(slots=True)
class LambdaZResult:
    """
    Stores the result of terminal phase analysis.
    """

    lambda_z: float | None
    slope: float | None
    intercept: float | None

    r: float | None
    r_squared: float | None
    adjusted_r_squared: float | None

    sse: float | None
    aic: float | None
    bic: float | None

    terminal_indices: list[int]
    terminal_times: list[float]
    terminal_concentrations: list[float]

    confidence: float | None
    status: str