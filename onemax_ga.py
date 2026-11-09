from __future__ import annotations
import time
from dataclasses import dataclass
import random
from typing import Callable, Sequence

try:
    import config  # Optional, ignored local overrides.
except ModuleNotFoundError:
    import importlib.util
    from pathlib import Path

    _config_path = Path(__file__).with_name("config.example.py")
    _config_spec = importlib.util.spec_from_file_location("config", _config_path)
    if _config_spec is None or _config_spec.loader is None:
        raise ImportError(f"Could not load example configuration at {_config_path}")
    config = importlib.util.module_from_spec(_config_spec)
    _config_spec.loader.exec_module(config)

Individual = list[int]
FitnessFunction = Callable[[Sequence[int]], float]
start_time = time.time()

def create_individual(length: int, rng: random.Random) -> Individual:
    return [rng.randint(0, 1) for _ in range(length)]


def create_population(size: int, length: int, rng: random.Random) -> list[Individual]:
    return [create_individual(length, rng) for _ in range(size)]


def fitness(individual: Sequence[int]) -> int:
    return sum(individual)


def evaluate_population(population: Sequence[Individual],
                        fitness_function: FitnessFunction = fitness) -> list[float]:
    return [fitness_function(individual) for individual in population]


def tournament_select(population: Sequence[Individual], fitnesses: Sequence[float],
                      tournament_size: int, rng: random.Random) -> Individual:
    contestants = rng.sample(range(len(population)), tournament_size)
    winner = max(contestants, key=lambda index: fitnesses[index])
    return population[winner]


def one_point_crossover(parent1: Sequence[int], parent2: Sequence[int],
                        crossover_rate: float, rng: random.Random) -> tuple[Individual, Individual]:
    if rng.random() >= crossover_rate or len(parent1) < 2:
        return list(parent1), list(parent2)
    cut = rng.randint(1, len(parent1) - 1)
    child1 = list(parent1[:cut]) + list(parent2[cut:])
    child2 = list(parent2[:cut]) + list(parent1[cut:])
    return child1, child2


def bit_flip_mutation(individual: Sequence[int], mutation_rate: float,
                      rng: random.Random) -> Individual:
    return [1 - bit if rng.random() < mutation_rate else bit for bit in individual]


def generational_replacement(population: Sequence[Individual], fitnesses: Sequence[float],
                             children: Sequence[Individual], elite_count: int) -> list[Individual]:
    ranked = sorted(range(len(population)), key=lambda index: fitnesses[index], reverse=True)
    next_population = [list(population[index]) for index in ranked[:elite_count]]
    next_population.extend(list(child) for child in children)
    return next_population


@dataclass
class GAResult:
    best_individual: Individual
    best_fitness: float
    success: bool
    generations: int
    best_fitness_history: list[float]
    average_fitness_history: list[float]


def run_ga(
    individual_length: int = config.INDIVIDUAL_LENGTH,
    population_size: int = config.POPULATION_SIZE,
    max_generations: int = config.MAX_GENERATIONS,
    crossover_rate: float = config.CROSSOVER_RATE,
    mutation_rate: float = config.MUTATION_RATE,
    tournament_size: int = config.TOURNAMENT_SIZE,
    elite_count: int = config.ELITE_COUNT,
    random_seed: int | None = config.RANDOM_SEED,
    fitness_function: FitnessFunction = fitness,
    target_fitness: float | None = config.TARGET_FITNESS,
) -> GAResult:
    if individual_length < 1 or population_size < 1:
        raise ValueError("individual_length and population_size must be positive")
    if max_generations < 0:
        raise ValueError("max_generations cannot be negative")
    if not 0 <= crossover_rate <= 1 or not 0 <= mutation_rate <= 1:
        raise ValueError("crossover_rate and mutation_rate must be between 0 and 1")
    if not 1 <= tournament_size <= population_size:
        raise ValueError("tournament_size must be between 1 and population_size")
    if not 0 <= elite_count <= population_size:
        raise ValueError("elite_count must be between 0 and population_size")

    rng = random.Random(random_seed)
    population = create_population(population_size, individual_length, rng)
    best_history: list[float] = []
    average_history = []
    generations = 0
    target = target_fitness
    if target is None and fitness_function is fitness:
        target = individual_length

    while True:
        fitnesses = evaluate_population(population, fitness_function)
        best_index = max(range(population_size), key=lambda index: fitnesses[index])
        best_score = fitnesses[best_index]
        best_history.append(best_score)
        average_history.append(sum(fitnesses) / population_size)

        if (target is not None and best_score >= target) or generations >= max_generations:
            break

        children = []
        children_needed = population_size - elite_count
        while len(children) < children_needed:
            parent1 = tournament_select(population, fitnesses, tournament_size, rng)
            parent2 = tournament_select(population, fitnesses, tournament_size, rng)
            child1, child2 = one_point_crossover(parent1, parent2, crossover_rate, rng)
            children.append(bit_flip_mutation(child1, mutation_rate, rng))
            if len(children) < children_needed:
                children.append(bit_flip_mutation(child2, mutation_rate, rng))

        population = generational_replacement(population, fitnesses, children, elite_count)
        generations += 1

    best_index = max(range(population_size), key=lambda index: fitnesses[index])
    return GAResult(
        best_individual=list(population[best_index]),
        best_fitness=fitnesses[best_index],
        success=target is not None and fitnesses[best_index] >= target,
        generations=generations,
        best_fitness_history=best_history,
        average_fitness_history=average_history,
    )

if __name__ == "__main__":
    result = run_ga()
    print("Best individual:", "".join(map(str, result.best_individual)))
    print("Best fitness:", result.best_fitness)
    print("Reached target:", result.success)
    print("Generations run:", result.generations)

    end_time = time.time()
    print("Time taken:", end_time - start_time)
