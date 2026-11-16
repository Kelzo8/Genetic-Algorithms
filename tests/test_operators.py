"""Tests for initialisation, variation and selection.

Randomised operators are checked over many seeds: whatever random choices
are made, the output must be a valid tree within the depth limits.
"""

import random
from collections import Counter

import pytest

from GP.gp_config import GPConfig
from GP.initialisation import ramped_half_and_half, random_tree
from GP.selection import tournament_selection
from GP.tree import depth
from GP.variation import subtree_crossover, subtree_mutation

from helpers import TERMINALS, is_valid_tree

SEEDS = range(200)


@pytest.mark.parametrize("d", [0, 1, 3, 5])
def test_full_trees_have_exact_depth(d):
    for seed in SEEDS:
        tree = random_tree(d, 'full', TERMINALS, rng=random.Random(seed))
        assert is_valid_tree(tree)
        assert depth(tree) == d


@pytest.mark.parametrize("d", [0, 1, 3, 5])
def test_grow_trees_within_depth(d):
    for seed in SEEDS:
        tree = random_tree(d, 'grow', TERMINALS, rng=random.Random(seed))
        assert is_valid_tree(tree)
        assert depth(tree) <= d


def test_ramped_half_and_half_population():
    config = GPConfig(population_size=60, min_init_depth=2, max_init_depth=4)
    pop = ramped_half_and_half(TERMINALS, config=config, rng=random.Random(0))
    assert len(pop) == 60
    assert all(is_valid_tree(t) and depth(t) <= 4 for t in pop)
    # Full trees at each depth guarantee every depth 2..4 appears.
    assert {2, 3, 4} <= {depth(t) for t in pop}


def test_same_seed_same_population():
    a = ramped_half_and_half(TERMINALS, rng=random.Random(5))
    b = ramped_half_and_half(TERMINALS, rng=random.Random(5))
    assert a == b


def test_crossover_valid_and_within_max_depth():
    rng = random.Random(1)
    for _ in SEEDS:
        p1 = random_tree(4, 'full', TERMINALS, rng=rng)
        p2 = random_tree(4, 'full', TERMINALS, rng=rng)
        child = subtree_crossover(p1, p2, max_depth=5, rng=rng)
        assert is_valid_tree(child)
        assert depth(child) <= 5


def test_crossover_rejects_too_deep_child():
    # Most donor subtrees are too deep for max_depth=1, so most children are
    # rejected; whatever happens, the result must respect the limit.
    p1 = ('+', 'x', 'y')
    p2 = ('+', ('+', ('+', 'x', 'x'), 'x'), ('+', ('+', 'x', 'x'), 'x'))  # depth 3
    for seed in SEEDS:
        child = subtree_crossover(p1, p2, max_depth=1, rng=random.Random(seed))
        assert depth(child) <= 1


def test_mutation_valid_and_within_max_depth():
    config = GPConfig(max_depth=6, mutation_subtree_depth=3)
    rng = random.Random(2)
    for _ in SEEDS:
        parent = random_tree(5, 'full', TERMINALS, rng=rng)
        child = subtree_mutation(parent, TERMINALS, config=config, rng=rng)
        assert is_valid_tree(child)
        assert depth(child) <= 6


def test_tournament_of_whole_population_picks_best():
    pop = ['a', 'b', 'c', 'd']
    fitnesses = [3.0, 0.5, 2.0, 9.0]
    for seed in range(20):
        assert tournament_selection(pop, fitnesses, 4, random.Random(seed)) == 'b'


def test_tournament_never_picks_worst_when_size_two_or_more():
    pop = list(range(10))
    fitnesses = [float(i) for i in pop]  # individual 9 is worst
    picks = Counter(tournament_selection(pop, fitnesses, 2, random.Random(s))
                    for s in range(500))
    assert picks[9] == 0
    assert picks[0] > picks[8]  # selection pressure favours better individuals
