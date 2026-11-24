import numpy as np

from .instance import TSPInstance


def generate_uniform_map(
    n_cities: int, seed: int, map_size: float = 100.0
) -> TSPInstance:
    """Generate city coordinates uniformly in the square ``[0, map_size)``."""
    if n_cities < 0:
        raise ValueError("n_cities must be non-negative")
    if map_size < 0:
        raise ValueError("map_size must be non-negative")
    coordinates = np.random.default_rng(seed).uniform(0.0, map_size, size=(n_cities, 2))
    return TSPInstance(coordinates)
