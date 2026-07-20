from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisResult:
    """
    Stores the results of a pharmacokinetic analysis.
    """

    # ---------- NCA Results ----------

    cmax: float | None = None
    tmax: float | None = None

    lambda_z: float | None = None
    t_half: float | None = None

    auc_0_t: float | None = None
    auc_0_inf: float | None = None

    aumc: float | None = None
    mrt: float | None = None

    cl: float | None = None
    vz: float | None = None

    # ---------- Metadata ----------

    analysis_mode: str = "NCA"

    route: str | None = None

    warnings: list[str] = field(default_factory=list)