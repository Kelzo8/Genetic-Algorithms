"""Symbolic regression problem: data and terminal set.

Each problem supplies its own terminals and fitness function, which are
passed into GP.genetic_programming(), so the engine stays problem-independent.
"""

# Hidden target function used to generate training outputs
# def target(x):
#     return x * x + x + 1

# Supplied input/output examples
TRAINING_DATA = [
    (1, 3),
    (2, 7),
    (3, 13),
    (4, 21),
    (5, 31)
]

# Terminal set: the input variable plus two constants
TERMINALS = ['x', 1, 2]
