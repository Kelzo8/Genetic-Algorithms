import math

from problem import TRAINING_DATA
from tree import evaluate


def fitness(tree):
    """Calculate mean absolute error against supplied examples."""

    try:
        error = sum(
            abs(evaluate(tree, x) - y)
            for x, y in TRAINING_DATA
        )

        if not math.isfinite(error):
            return math.inf

        return error / len(TRAINING_DATA)

    except (OverflowError, ValueError, ZeroDivisionError):
        return math.inf