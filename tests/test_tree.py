"""Tests for tree evaluation and the helpers used by the variation operators."""

import numpy as np

from GP.tree import (depth, evaluate, get_subtree, node_paths,
                     replace_subtree, size, to_string)

# (x * x) + (y - 1)
TREE = ('+', ('*', 'x', 'x'), ('-', 'y', 1))


def test_evaluate_scalars():
    assert evaluate(TREE, {'x': 3, 'y': 5}) == 13


def test_evaluate_arrays_scores_every_element():
    out = evaluate(TREE, {'x': np.array([0.0, 1.0, 2.0]), 'y': np.array([1.0, 1.0, 1.0])})
    np.testing.assert_allclose(out, [0.0, 1.0, 4.0])


def test_evaluate_terminals():
    assert evaluate('x', {'x': 7}) == 7
    assert evaluate(2.5, {}) == 2.5


def test_depth_and_size():
    assert depth('x') == 0 and size('x') == 1
    assert depth(TREE) == 2
    assert size(TREE) == 7


def test_node_paths_visits_every_node_once():
    paths = list(node_paths(TREE))
    assert len(paths) == size(TREE)
    assert len(set(paths)) == len(paths)
    assert paths[0] == ()  # the root comes first


def test_get_subtree():
    assert get_subtree(TREE, ()) == TREE
    assert get_subtree(TREE, (1,)) == ('*', 'x', 'x')
    assert get_subtree(TREE, (2, 2)) == 1


def test_replace_subtree_returns_new_tree():
    new = replace_subtree(TREE, (2, 1), 'x')
    assert new == ('+', ('*', 'x', 'x'), ('-', 'x', 1))
    assert TREE == ('+', ('*', 'x', 'x'), ('-', 'y', 1))  # original untouched


def test_replace_root():
    assert replace_subtree(TREE, (), 'y') == 'y'


def test_to_string():
    assert to_string(TREE) == "((x * x) + (y - 1))"
    assert to_string(('neg', 'x')) == "neg(x)"
