from dataclasses import dataclass, field


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

    fitted_times: list[float] = field(default_factory=list)
    fitted_concentrations: list[float] = field(default_factory=list)

    rmse: float | None = None
    mae: float | None = None
    bias: float | None = None