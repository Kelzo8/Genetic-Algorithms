"""The generational GP loop, independent of any particular problem."""

import math
import random
from dataclasses import dataclass, field

from .gp_config import DEFAULT_CONFIG
from .initialisation import ramped_half_and_half
from .primitives import FUNCTIONS
from .tree import size, to_string
from .selection import tournament_selection
from .variation import (
    subtree_crossover,
    subtree_mutation
)


@dataclass
class GPResult:
    """Outcome of one GP run. Fitness is minimised (lower is better)."""
    best: object
    best_fitness: float
    generations: int
    success: bool
    evaluations: int = 0               # calls made to fitness_fn in total
    best_fitness_history: list = field(default_factory=list)
    avg_size_history: list = field(default_factory=list)
    evaluations_history: list = field(default_factory=list)  # cumulative, per generation


class FitnessEvaluator:
    """Wraps fitness_fn to count calls and (optionally) cache results.

    Trees are nested tuples, which are hashable, so they can be dict keys.
    Elites and reproduced parents reappear every generation, and crossover
    often recreates trees already seen; the cache skips re-evaluating them.
    `evaluations` counts real calls to fitness_fn, so random search can be
    given exactly the same budget.
    """

    def __init__(self, fitness_fn, use_cache=True):
        self.fitness_fn = fitness_fn
        self.use_cache = use_cache
        self.cache = {}
        self.evaluations = 0

    def __call__(self, tree):
        if self.use_cache and tree in self.cache:
            return self.cache[tree]

        value = float(self.fitness_fn(tree))
        self.evaluations += 1

        # NaN compares False with everything, which would corrupt min() and
        # sorting, so treat it as the worst possible fitness.
        if math.isnan(value):
            value = math.inf

        if self.use_cache:
            self.cache[tree] = value

        return value


def genetic_programming(fitness_fn, terminals, functions=FUNCTIONS,
                        config=DEFAULT_CONFIG, verbose=True):
    """Run GP for any problem.

    fitness_fn(tree) -> float (lower is better); terminals and functions
    define the primitive set; config (a GPConfig) holds every parameter,
    including the seed. Returns a GPResult with per-generation history
    for convergence curves.
    """

    # One private generator per run: the run is reproducible from
    # config.seed alone, and other code using `random` cannot disturb it.
    rng = random.Random(config.seed)
    evaluate_fitness = FitnessEvaluator(fitness_fn, config.cache_fitness)

    # Generate initial population
    population = ramped_half_and_half(terminals, functions, config, rng)

    best_history = []
    size_history = []
    evaluations_history = []
    generation = 0

    while True:

        # Evaluate every individual
        fitnesses = [
            evaluate_fitness(tree) for tree in population
        ]

        # Find the best individual
        best_idx = min(
            range(len(population)),
            key=lambda i: fitnesses[i]
        )

        best = population[best_idx]

        # Calculate average tree size
        avg_size = sum(
            size(tree) for tree in population
        ) / len(population)

        best_history.append(fitnesses[best_idx])
        size_history.append(avg_size)
        evaluations_history.append(evaluate_fitness.evaluations)

        # Display generation statistics
        if verbose:
            print(
                f"Gen {generation:2d} | "
                f"fitness = {fitnesses[best_idx]:.6f} | "
                f"avg size = {avg_size:5.1f} | "
                f"evals = {evaluate_fitness.evaluations:6d} | "
                f"{to_string(best)}"
            )

        # Stop if a good enough solution was found or the budget is used up
        success = (config.target_fitness is not None
                   and fitnesses[best_idx] < config.target_fitness)

        if success or generation >= config.max_generations:
            if verbose:
                if success:
                    print(f"\nTarget reached in generation {generation}:")
                else:
                    print("\nReached the generation limit.")
                print(f"  {to_string(best)} (fitness = {fitnesses[best_idx]:.6f})")

            return GPResult(
                best=best,
                best_fitness=fitnesses[best_idx],
                generations=generation,
                success=success,
                evaluations=evaluate_fitness.evaluations,
                best_fitness_history=best_history,
                avg_size_history=size_history,
                evaluations_history=evaluations_history,
            )

        # Elitism: preserve the best individuals
        ranked = sorted(
            range(len(population)),
            key=lambda i: fitnesses[i]
        )

        next_population = [
            population[i] for i in ranked[:config.elitism]
        ]

        # Generate offspring to fill the next population
        while len(next_population) < config.population_size:

            r = rng.random()

            parent = tournament_selection(
                population,
                fitnesses,
                config.tournament_size,
                rng
            )

            if r < config.crossover_rate:

                other = tournament_selection(
                    population,
                    fitnesses,
                    config.tournament_size,
                    rng
                )

                child = subtree_crossover(
                    parent,
                    other,
                    config.max_depth,
                    rng
                )

            elif r < config.crossover_rate + config.mutation_rate:

                child = subtree_mutation(parent, terminals, functions,
                                         config, rng)

            else:

                # Reproduction: copy the selected parent
                child = parent

            next_population.append(child)

        # Replace old population
        population = next_population
        generation += 1
