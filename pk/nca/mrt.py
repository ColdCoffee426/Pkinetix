def calculate(
    auc: float | None,
    aumc: float | None,
) -> float | None:
    """
    Calculate Mean Residence Time.
    """

    if auc is None:
        return None

    if aumc is None:
        return None

    if auc <= 0:
        return None

    return aumc / auc