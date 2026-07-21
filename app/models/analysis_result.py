from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisResult:
    """
    Stores the complete results of a pharmacokinetic analysis.
    """

    # NCA Parameters
    cmax: float | None = None
    tmax: float | None = None

    lambda_z: float | None = None
    t_half: float | None = None

    auc_0_t: float | None = None
    auc_0_inf: float | None = None
    auc_extrapolated: float | None = None
    auc_extrapolated_percent: float | None = None

    aumc: float | None = None
    mrt: float | None = None

    cl: float | None = None
    vz: float | None = None

    # Terminal Phase Information
    terminal_points: list[int] = field(default_factory=list)
    terminal_r_squared: float | None = None
    terminal_adjusted_r_squared: float | None = None
    terminal_sse: float | None = None
    terminal_aic: float | None = None
    terminal_bic: float | None = None
    terminal_confidence: float | None = None

    # Analysis Information
    analysis_mode: str = "NCA"
    route: str | None = None

    # Messages
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def has_results(self) -> bool:
        """
        Returns True if at least one PK parameter has been calculated.
        """

        return any(
            value is not None
            for value in (
                self.cmax,
                self.tmax,
                self.lambda_z,
                self.auc_0_t,
            )
        )
    @property
    def has_terminal_phase(self) -> bool:
        """
        Returns True if a terminal phase was identified.
        """

        return (
            self.lambda_z is not None
        )