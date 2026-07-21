from app.models.project import Project


def calculate(
    project: Project,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate clearance.

    IV:
        CL = Dose / AUC∞

    Extravascular:
        CL/F = Dose / AUC∞
    """

    if auc_0_inf is None:
        return None

    if auc_0_inf <= 0:
        return None

    if project.dose is None:
        return None

    return project.dose / auc_0_inf