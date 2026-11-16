from .primitives import FUNCTIONS


def children(tree):
    """Return the children of a tree node."""
    if isinstance(tree, tuple):
        return tree[1:]
    return []


def evaluate(tree, env, functions=FUNCTIONS):
    """Evaluate an expression tree.

    env maps terminal names to values, e.g. {'x': 3} or
    {'dist_current': array([...]), ...}. Numeric terminals are constants.
    """
    if isinstance(tree, tuple):
        op, *args = tree
        func, _arity = functions[op]

        return func(
            *(evaluate(child, env, functions) for child in args)
        )

    if isinstance(tree, str):
        return env[tree]

    return tree


def depth(tree):
    """Calculate the maximum depth of a tree."""
    if isinstance(tree, tuple):
        kids = children(tree)

        return 1 + max(
            (depth(child) for child in kids),
            default=0
        )

    return 0


def size(tree):
    """Calculate the total number of nodes in a tree."""
    if isinstance(tree, tuple):
        return 1 + sum(
            size(child) for child in children(tree)
        )

    return 1


def to_string(tree):
    """Convert an expression tree into a readable string."""
    if isinstance(tree, tuple):
        op, *args = tree

        rendered = [
            to_string(arg) for arg in args
        ]

        if len(args) == 1:
            return f"{op}({rendered[0]})"

        if len(args) == 2 and op in {'+', '-', '*', '/'}:
            return f"({rendered[0]} {op} {rendered[1]})"

        return f"{op}({', '.join(rendered)})"

    return str(tree)


def node_paths(tree, path=()):
    """Generate the paths to every node in a tree."""
    yield path

    if isinstance(tree, tuple):
        for i, child in enumerate(children(tree), start=1):
            yield from node_paths(child, path + (i,))


def get_subtree(tree, path):
    """Retrieve a subtree using its path."""
    for index in path:
        tree = tree[index]

    return tree


def replace_subtree(tree, path, new_subtree):
    """Replace a subtree at a specified path."""
    if not path:
        return new_subtree

    node = list(tree)

    node[path[0]] = replace_subtree(
        tree[path[0]],
        path[1:],
        new_subtree
    )

    return tuple(node)
