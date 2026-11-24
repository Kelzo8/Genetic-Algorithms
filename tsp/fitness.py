import math
from collections.abc import Callable, Iterable, Mapping, Sequence

from .constructor import construct_tour
from .instance import TSPInstance


def make_fitness_function(
    training_instances: Iterable[TSPInstance],
    terminals: Sequence[object],
    functions: Mapping[str, tuple[Callable[..., object], int]],
) -> Callable[[object], float]:
    """Return mean tour length for GP's lower-is-better fitness convention."""
    instances = tuple(training_instances)
    if not instances:
        raise ValueError("training_instances must not be empty")

    def fitness(tree) -> float:
        try:
            lengths = [
                instance.tour_length(construct_tour(tree, instance, terminals, functions))
                for instance in instances
            ]
            mean_length = math.fsum(lengths) / len(lengths)
            if not math.isfinite(mean_length) or mean_length <= 0.0:
                return math.inf
            return mean_length
        except (ArithmeticError, KeyError, TypeError, ValueError):
            return math.inf

    return fitness
