
import random

from gp_config import TOURNAMENT_SIZE


def tournament_selection(population, fitnesses, tournament_size=TOURNAMENT_SIZE):
    """Select the individual with the best fitness from a random tournament."""

    contestants = random.sample(
        range(len(population)),
        tournament_size
    )

    winner = min(
        contestants,
        key=lambda i: fitnesses[i]
    )

    return population[winner]
