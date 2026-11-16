import random
from gp_config import MAX_DEPTH, MUTATION_SUBTREE_DEPTH
from primitives import FUNCTIONS
from tree import (
    depth,
    node_paths,
    get_subtree,
    replace_subtree
)
from initialisation import random_tree


def subtree_crossover(parent1, parent2):
    """Replace a random subtree of parent1 with one from parent2."""

    point1 = random.choice(
        list(node_paths(parent1))
    )

    point2 = random.choice(
        list(node_paths(parent2))
    )

    child = replace_subtree(
        parent1,
        point1,
        get_subtree(parent2, point2)
    )

    # Reject offspring that exceed the maximum depth
    if depth(child) <= MAX_DEPTH:
        return child

    return parent1


def subtree_mutation(parent, terminals, functions=FUNCTIONS):
    """Replace a random subtree with a newly generated tree."""

    point = random.choice(
        list(node_paths(parent))
    )

    child = replace_subtree(
        parent,
        point,
        random_tree(MUTATION_SUBTREE_DEPTH, 'grow', terminals, functions)
    )

    # Reject offspring that exceed the maximum depth
    if depth(child) <= MAX_DEPTH:
        return child

    return parent
