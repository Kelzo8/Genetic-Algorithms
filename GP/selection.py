"""Parent selection."""

import random

from .gp_config import DEFAULT_CONFIG


def tournament_selection(population, fitnesses,
                         tournament_size=DEFAULT_CONFIG.tournament_size,
                         rng=random):
    """Select the individual with the best (lowest) fitness from a random
    tournament of `tournament_size` distinct individuals."""

    contestants = rng.sample(
        range(len(population)),
        tournament_size
    )

    winner = min(
        contestants,
        key=lambda i: fitnesses[i]
    )

    return population[winner]
