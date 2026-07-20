from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisResult:
    """
    Stores the output of a pharmacokinetic analysis.
    """

    # NCA part


    cmax: float | None = None
    tmax: float | None = None

    auc_0_t: float | None = None
    auc_0_inf: float | None = None

    lambda_z: float | None = None

    half_life: float | None = None

    aumc: float | None = None

    mrt: float | None = None

    clearance: float | None = None

    volume: float | None = None

    #Metadata 
    warnings: list[str] = field(default_factory=list)

    analysis_mode: str = "NCA"

    route: str | None = None