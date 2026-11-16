"""Tests for the GP loop, its config, and the fitness cache/counter."""

import math
from dataclasses import replace

import pytest

from GP import GPConfig, genetic_programming
from GP.algorithm import FitnessEvaluator
from GP.tree import size
from symreg.fitness import fitness as symreg_fitness

from helpers import TERMINALS

# Small, fast config with no early stopping.
SMALL = GPConfig(population_size=30, max_generations=8, target_fitness=None)


def size_fitness(tree):
    """Deterministic toy fitness: smaller trees are better."""
    return float(size(tree))


def test_same_seed_gives_identical_run():
    a = genetic_programming(size_fitness, TERMINALS, config=SMALL, verbose=False)
    b = genetic_programming(size_fitness, TERMINALS, config=SMALL, verbose=False)
    assert a == b


def test_history_has_one_entry_per_generation():
    r = genetic_programming(size_fitness, TERMINALS, config=SMALL, verbose=False)
    # Generation 0 (initial population) plus max_generations more.
    assert r.generations == SMALL.max_generations
    for history in (r.best_fitness_history, r.avg_size_history, r.evaluations_history):
        assert len(history) == SMALL.max_generations + 1


def test_elitism_means_best_never_gets_worse():
    r = genetic_programming(size_fitness, TERMINALS, config=SMALL, verbose=False)
    h = r.best_fitness_history
    assert all(later <= earlier for earlier, later in zip(h, h[1:]))


def test_stops_early_at_target():
    config = GPConfig(population_size=50, max_generations=50, target_fitness=1.5)
    r = genetic_programming(size_fitness, TERMINALS, config=config, verbose=False)
    assert r.success and r.best_fitness < 1.5  # found a single terminal (size 1)
    assert r.generations < 50


def test_solves_simple_symbolic_regression():
    r = genetic_programming(symreg_fitness, ['x', 1, 2], verbose=False)
    assert r.success


def test_without_cache_every_individual_is_evaluated():
    config = GPConfig(population_size=30, max_generations=8, target_fitness=None,
                      cache_fitness=False)
    r = genetic_programming(size_fitness, TERMINALS, config=config, verbose=False)
    assert r.evaluations == 30 * 9


def test_cache_saves_evaluations_but_not_results():
    cached = genetic_programming(size_fitness, TERMINALS, config=SMALL, verbose=False)
    uncached = genetic_programming(
        size_fitness, TERMINALS, config=replace(SMALL, cache_fitness=False),
        verbose=False)
    assert cached.evaluations < uncached.evaluations
    # Fitness is deterministic, so caching must not change the run itself.
    assert cached.best == uncached.best
    assert cached.best_fitness_history == uncached.best_fitness_history


def test_evaluator_counts_and_caches():
    calls = []
    evaluator = FitnessEvaluator(lambda t: calls.append(t) or 1.0)
    evaluator(('+', 'x', 1))
    evaluator(('+', 'x', 1))
    evaluator('x')
    assert evaluator.evaluations == 2
    assert len(calls) == 2


def test_evaluator_turns_nan_into_inf():
    evaluator = FitnessEvaluator(lambda t: float('nan'))
    assert evaluator('x') == math.inf


@pytest.mark.parametrize("bad", [
    dict(crossover_rate=0.8, mutation_rate=0.5),
    dict(tournament_size=0),
    dict(population_size=10, tournament_size=11),
    dict(population_size=10, elitism=10),
    dict(min_init_depth=5, max_init_depth=4),
    dict(max_init_depth=9, max_depth=8),
])
def test_config_rejects_invalid_settings(bad):
    with pytest.raises(ValueError):
        GPConfig(**bad)
