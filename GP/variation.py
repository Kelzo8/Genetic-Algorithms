"""Variation operators: subtree crossover and subtree mutation.

Both reject (return the parent unchanged) any child deeper than max_depth,
which is the bloat control.
"""

import random

from .gp_config import DEFAULT_CONFIG
from .primitives import FUNCTIONS
from .tree import (
    depth,
    node_paths,
    get_subtree,
    replace_subtree
)
from .initialisation import random_tree


def subtree_crossover(parent1, parent2, max_depth=DEFAULT_CONFIG.max_depth,
                      rng=random):
    """Replace a random subtree of parent1 with one from parent2."""

    point1 = rng.choice(
        list(node_paths(parent1))
    )

    point2 = rng.choice(
        list(node_paths(parent2))
    )

    child = replace_subtree(
        parent1,
        point1,
        get_subtree(parent2, point2)
    )

    # Reject offspring that exceed the maximum depth
    if depth(child) <= max_depth:
        return child

    return parent1


def subtree_mutation(parent, terminals, functions=FUNCTIONS,
                     config=DEFAULT_CONFIG, rng=random):
    """Replace a random subtree with a newly generated 'grow' tree."""

    point = rng.choice(
        list(node_paths(parent))
    )

    child = replace_subtree(
        parent,
        point,
        random_tree(config.mutation_subtree_depth, 'grow', terminals,
                    functions, config.terminal_prob, rng)
    )

    # Reject offspring that exceed the maximum depth
    if depth(child) <= config.max_depth:
        return child

    return parent
