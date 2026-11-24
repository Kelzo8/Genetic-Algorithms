from collections.abc import Callable, Mapping, Sequence

import numpy as np

from GP.tree import evaluate
from .features import candidate_features
from .instance import TSPInstance


def construct_tour(
    tree: object,
    instance: TSPInstance,
    terminals: Sequence[object],
    functions: Mapping[str, tuple[Callable[..., object], int]],
) -> list[int]:
    """Build a closed tour, selecting the highest-scoring unvisited city."""
    if instance.n_cities == 0:
        raise ValueError("cannot construct a tour for an instance with no cities")

    start_city = current_city = 0
    unvisited = set(range(1, instance.n_cities))
    distances = instance.distance_matrix()
    tour = [start_city]

    while unvisited:
        candidates = sorted(unvisited)
        features = candidate_features(
            instance, current_city, start_city, candidates, distances
        )
        env = {
            terminal: np.asarray([features[city][terminal] for city in candidates])
            for terminal in terminals
            if isinstance(terminal, str) and terminal in features[candidates[0]]
        }
        priorities = np.asarray(evaluate(tree, env, functions), dtype=float)
        if priorities.ndim == 0:
            priorities = np.full(len(candidates), float(priorities))
        priorities = np.broadcast_to(priorities, (len(candidates),))
        priorities = np.nan_to_num(priorities, nan=-np.inf)
        selected = candidates[int(np.argmax(priorities))]
        tour.append(selected)
        unvisited.remove(selected)
        current_city = selected

    tour.append(start_city)
    return tour
