import math


def rmse(
    observed: list[float],
    predicted: list[float],
) -> float:
    error = sum(
        (o - p) ** 2
        for o, p in zip(observed, predicted)
    )
    return math.sqrt(error / len(observed))


def mae(
    observed: list[float],
    predicted: list[float],
) -> float:
    return sum(
        abs(o - p)
        for o, p in zip(observed, predicted)
    ) / len(observed)


def bias(
    observed: list[float],
    predicted: list[float],
) -> float:
    return sum(
        p - o
        for o, p in zip(observed, predicted)
    ) / len(observed)
