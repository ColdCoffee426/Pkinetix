from app.models.project import Project


def calculate(
    project: Project,
    auc_0_inf: float | None,
) -> float | None:
    """
    Calculate clearance in L per selected time unit.

    Dose is currently stored in mg.
    """

    if (
        project.dose is None
        or project.dose <= 0
        or auc_0_inf is None
        or auc_0_inf <= 0
    ):
        return None

    concentration_unit = project.units.concentration

    if concentration_unit == "ng/mL":
        return project.dose * 1000 / auc_0_inf

    if concentration_unit == "µg/mL":
        return project.dose / auc_0_inf

    return None