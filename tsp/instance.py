from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TSPInstance:
    """A TSP instance represented by an ``(n, 2)`` coordinate array."""

    coordinates: np.ndarray

    def __post_init__(self) -> None:
        coordinates = np.array(self.coordinates, dtype=float, copy=True)
        if coordinates.ndim != 2 or coordinates.shape[1] != 2:
            raise ValueError("coordinates must have shape (n_cities, 2)")
        if not np.isfinite(coordinates).all():
            raise ValueError("coordinates must contain only finite values")
        coordinates.setflags(write=False)
        object.__setattr__(self, "coordinates", coordinates)

    @property
    def n_cities(self) -> int:
        """Number of cities in this instance."""
        return int(self.coordinates.shape[0])

    def distance_matrix(self) -> np.ndarray:
        """Return the symmetric matrix of pairwise Euclidean distances."""
        differences = (
            self.coordinates[:, np.newaxis, :]
            - self.coordinates[np.newaxis, :, :]
        )
        return np.linalg.norm(differences, axis=2)

    def tour_length(self, tour: list[int]) -> float:
        """Return the closed-tour length, adding the return edge if needed."""
        if len(tour) < 2:
            return 0.0
        indices = np.asarray(tour, dtype=int)
        points = self.coordinates[indices]
        edges = points - np.roll(points, -1, axis=0)
        return float(np.linalg.norm(edges, axis=1).sum())
