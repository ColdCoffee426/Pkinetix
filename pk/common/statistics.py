from app.models.regression_result import RegressionResult


def regression_score(
    regression: RegressionResult,
    point_count: int,
) -> float:
    """
    Calculate an overall quality score for a regression.
    Higher scores indicate better terminal phases.
    """

    score = 0.0

    score += (
        regression.adjusted_r_squared
        * 1000
    )

    score -= regression.aic

    score -= (
        regression.bic
        * 0.5
    )

    score += (
        point_count
        * 2
    )

    return score