"""Shared test helpers."""

from GP.primitives import FUNCTIONS

TERMINALS = ['x', 'y', 1, 2]


def is_valid_tree(tree, terminals=TERMINALS, functions=FUNCTIONS):
    """True if every function node has a known op with the right number of
    children, and every leaf is one of the allowed terminals."""
    if isinstance(tree, tuple):
        op, *args = tree
        return (op in functions
                and len(args) == functions[op][1]
                and all(is_valid_tree(a, terminals, functions) for a in args))
    return tree in terminals
