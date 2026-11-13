
import random

from config import TOURNAMENT_SIZE


def tournament_selection(population, fitnesses):
    """Select the individual with the best fitness from a random tournament."""

    contestants = random.sample(
        range(len(population)),
        TOURNAMENT_SIZE
    )

    winner = min(
        contestants,
        key=lambda i: fitnesses[i]
    )

    return population[winner]
