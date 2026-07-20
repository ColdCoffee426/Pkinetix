from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class RegressionResult:
    """
    Stores the results of a simple linear regression.
    """

    slope: float
    intercept: float
    r_value: float
    r_squared: float


def linear_regression(
    x: np.ndarray,
    y: np.ndarray,
) -> RegressionResult:
    """
    Perform simple linear regression.

    Parameters
    ----------
    x
        Independent variable.

    y
        Dependent variable.

    Returns
    -------
    RegressionResult
    """

    slope, intercept = np.polyfit(x, y, 1)

    correlation_matrix = np.corrcoef(x, y)

    r = correlation_matrix[0, 1]

    return RegressionResult(
        slope=slope,
        intercept=intercept,
        r_value=r,
        r_squared=r ** 2,
    )