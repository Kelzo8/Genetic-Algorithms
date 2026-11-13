import random
from config import (
    POPULATION_SIZE,
    MAX_GENERATIONS,
    CROSSOVER_RATE,
    MUTATION_RATE,
    ELITISM,
    TARGET_FITNESS
)
from initialisation import ramped_half_and_half
from fitness import fitness
from tree import size, to_string
from selection import tournament_selection
from variation import (
    subtree_crossover,
    subtree_mutation
)


def genetic_programming():

    # Generate initial population
    population = ramped_half_and_half()

    for generation in range(MAX_GENERATIONS):

        # Evaluate every individual
        fitnesses = [
            fitness(tree) for tree in population
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

        # Display generation statistics
        print(
            f"Gen {generation:2d} | "
            f"error = {fitnesses[best_idx]:.6f} | "
            f"avg size = {avg_size:5.1f} | "
            f"{to_string(best)}"
        )

        # Check whether a perfect solution was found
        if fitnesses[best_idx] < TARGET_FITNESS:

            print(
                f"\nPerfect program found in generation {generation}:"
            )

            print(f"  {to_string(best)}")

            return best

        # Elitism: preserve the best individuals
        ranked = sorted(
            range(len(population)),
            key=lambda i: fitnesses[i]
        )

        next_population = [
            population[i] for i in ranked[:ELITISM]
        ]

        # Generate offspring to fill the next population
        while len(next_population) < POPULATION_SIZE:

            r = random.random()

            parent = tournament_selection(
                population,
                fitnesses
            )

            if r < CROSSOVER_RATE:

                other = tournament_selection(
                    population,
                    fitnesses
                )

                child = subtree_crossover(
                    parent,
                    other
                )

            elif r < CROSSOVER_RATE + MUTATION_RATE:

                child = subtree_mutation(parent)

            else:

                # Reproduction: copy the selected parent
                child = parent

            next_population.append(child)

        # Replace old population
        population = next_population

    # Find the best individual after the final generation
    final_fitnesses = [
        fitness(tree) for tree in population
    ]

    best_idx = min(
        range(len(population)),
        key=lambda i: final_fitnesses[i]
    )

    best = population[best_idx]

    print("\nReached the generation limit.")

    print(
        f"Best program: {to_string(best)} "
        f"(error = {final_fitnesses[best_idx]:.6f})"
    )

    return best
