import random
from dataclasses import dataclass, field

from gp_config import (
    POPULATION_SIZE,
    MAX_GENERATIONS,
    CROSSOVER_RATE,
    MUTATION_RATE,
    ELITISM,
    TARGET_FITNESS
)
from initialisation import ramped_half_and_half
from primitives import FUNCTIONS
from tree import size, to_string
from selection import tournament_selection
from variation import (
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
    best_fitness_history: list = field(default_factory=list)
    avg_size_history: list = field(default_factory=list)


def genetic_programming(fitness_fn, terminals, functions=FUNCTIONS,
                        population_size=POPULATION_SIZE,
                        max_generations=MAX_GENERATIONS,
                        crossover_rate=CROSSOVER_RATE,
                        mutation_rate=MUTATION_RATE,
                        elitism=ELITISM,
                        target_fitness=TARGET_FITNESS,
                        verbose=True):
    """Run GP for any problem.

    fitness_fn(tree) -> float (lower is better); terminals and functions
    define the primitive set. Set target_fitness=None to always run the full
    number of generations. Returns a GPResult with per-generation history
    for convergence curves.
    """

    # Generate initial population
    population = ramped_half_and_half(terminals, functions, population_size)

    best_history = []
    size_history = []
    generation = 0

    while True:

        # Evaluate every individual
        fitnesses = [
            fitness_fn(tree) for tree in population
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

        # Display generation statistics
        if verbose:
            print(
                f"Gen {generation:2d} | "
                f"fitness = {fitnesses[best_idx]:.6f} | "
                f"avg size = {avg_size:5.1f} | "
                f"{to_string(best)}"
            )

        # Stop if a good enough solution was found or the budget is used up
        success = (target_fitness is not None
                   and fitnesses[best_idx] < target_fitness)

        if success or generation >= max_generations:
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
                best_fitness_history=best_history,
                avg_size_history=size_history,
            )

        # Elitism: preserve the best individuals
        ranked = sorted(
            range(len(population)),
            key=lambda i: fitnesses[i]
        )

        next_population = [
            population[i] for i in ranked[:elitism]
        ]

        # Generate offspring to fill the next population
        while len(next_population) < population_size:

            r = random.random()

            parent = tournament_selection(
                population,
                fitnesses
            )

            if r < crossover_rate:

                other = tournament_selection(
                    population,
                    fitnesses
                )

                child = subtree_crossover(
                    parent,
                    other
                )

            elif r < crossover_rate + mutation_rate:

                child = subtree_mutation(parent, terminals, functions)

            else:

                # Reproduction: copy the selected parent
                child = parent

            next_population.append(child)

        # Replace old population
        population = next_population
        generation += 1
