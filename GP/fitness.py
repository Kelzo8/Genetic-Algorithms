import math

from problem import TRAINING_DATA
from tree import evaluate


def fitness(tree, data=TRAINING_DATA):
    """Mean absolute error against supplied examples (lower is better)."""

    try:
        error = sum(
            abs(evaluate(tree, {'x': x}) - y)
            for x, y in data
        )

        if not math.isfinite(error):
            return math.inf

        return error / len(data)

    except (OverflowError, ValueError, ZeroDivisionError):
        return math.inf
