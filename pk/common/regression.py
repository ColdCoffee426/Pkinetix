import math

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
    x
        Independent variable.

    y
        Dependent variable.

    Returns
    -------
    RegressionResult
        Regression statistics.
    """

    if len(x) != len(y):
        raise ValueError(
            "x and y must have the same length."
        )

    if len(x) < 2:
        raise ValueError(
            "At least two points are required."
        )

    x_array = np.asarray(x, dtype=float)
    y_array = np.asarray(y, dtype=float)

    slope, intercept = np.polyfit(
        x_array,
        y_array,
        1,
    )

    predicted = (
        slope * x_array
        + intercept
    )

    residuals = (
        y_array
        - predicted
    )

    sse = float(
        np.sum(
            residuals ** 2
        )
    )

    r = float(
        np.corrcoef(
            x_array,
            y_array,
        )[0, 1]
    )

    if np.isnan(r):
        r = 0.0

    r_squared = r ** 2

    n = len(x_array)
    p = 1

    if n > p + 1:
        adjusted_r_squared = (
            1
            - (1 - r_squared)
            * (n - 1)
            / (n - p - 1)
        )
    else:
        adjusted_r_squared = r_squared

    mse = max(
        sse / n,
        1e-12,
    )

    aic = (
        n * math.log(mse)
        + 2 * (p + 1)
    )

    bic = (
        n * math.log(mse)
        + math.log(n)
        * (p + 1)
    )

    return RegressionResult(
        slope=float(slope),
        intercept=float(intercept),
        r=r,
        r_squared=r_squared,
        adjusted_r_squared=adjusted_r_squared,
        sse=sse,
        aic=aic,
        bic=bic,
    )