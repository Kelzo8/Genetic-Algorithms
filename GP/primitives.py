"""Default function set.

Functions work on plain numbers and, if NumPy is installed, on NumPy arrays,
so a tree can score many cases (e.g. every candidate city) in one evaluation.
Terminal sets are problem-specific and live with each problem.
"""

import operator

try:
    import numpy as np
except ImportError:  # NumPy is optional for scalar-only problems
    np = None


def protected_div(a, b):
    """Division that returns 1.0 instead of failing when |b| is tiny."""
    if np is not None and (isinstance(a, np.ndarray) or isinstance(b, np.ndarray)):
        b = np.asarray(b, dtype=float)
        safe = np.abs(b) > 1e-6
        return np.where(safe, np.divide(a, np.where(safe, b, 1.0)), 1.0)
    return a / b if abs(b) > 1e-6 else 1.0


FUNCTIONS = {
    '+': (operator.add, 2),
    '-': (operator.sub, 2),
    '*': (operator.mul, 2),
    '/': (protected_div, 2),
    'neg': (operator.neg, 1),
}
