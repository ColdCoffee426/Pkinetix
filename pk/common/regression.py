import numpy as np

from app.models.regression_result import RegressionResult


def linear_regression(
    x: list[float],
    y: list[float],
) -> RegressionResult:
    """
    Perform simple linear regression.

    Parameters
    ----------
    x : list[float]
        Independent variable.

    y : list[float]
        Dependent variable.

    Returns
    -------
    RegressionResult
        Regression statistics.
    """

    x_array = np.asarray(x, dtype=float)
    y_array = np.asarray(y, dtype=float)

    slope, intercept = np.polyfit(x_array, y_array, 1)

    r = np.corrcoef(x_array, y_array)[0, 1]

    return RegressionResult(
        slope=slope,
        intercept=intercept,
        r=r,
        r_squared=r**2,
    )