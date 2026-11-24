from collections.abc import Iterable

import numpy as np

from .instance import TSPInstance


def candidate_features(
    instance: TSPInstance,
    current_city: int,
    start_city: int,
    unvisited: Iterable[int],
    distances: np.ndarray,
) -> dict[int, dict[str, float]]:
    """Compute ``D_cn``, ``D_in`` and ``D_c`` for each unvisited candidate.

    ``D_c`` measures from the current city to the centroid of all remaining
    unvisited cities after the candidate is removed.
    """
    candidates = np.asarray(list(unvisited), dtype=int)
    if candidates.size == 0:
        return {}

    coordinates = instance.coordinates
    current = coordinates[current_city]
    candidate_points = coordinates[candidates]
    count = len(candidates)

    d_cn = np.asarray(distances[current_city, candidates], dtype=float)
    d_in = np.asarray(distances[start_city, candidates], dtype=float)
    if count == 1:
        d_c = np.zeros(1, dtype=float)
    else:
        remaining_sums = coordinates[candidates].sum(axis=0) - candidate_points
        centroids = remaining_sums / (count - 1)
        d_c = np.linalg.norm(centroids - current, axis=1)

    return {
        int(city): {
            "D_cn": float(d_cn[i]),
            "D_in": float(d_in[i]),
            "D_c": float(d_c[i]),
        }
        for i, city in enumerate(candidates)
    }
