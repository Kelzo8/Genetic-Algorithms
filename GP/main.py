import random

from gp_config import SEED
from algorithm import genetic_programming
from fitness import fitness
from problem import TERMINALS


if __name__ == "__main__":

    random.seed(SEED)

    result = genetic_programming(fitness, TERMINALS)

    print("Final solution:", result.best)

    try:
        from visualisation import visualise_tree
        visualise_tree(result.best, "gp_tree")
    except Exception as exc:  # Graphviz missing or no display available
        print(f"(Skipped tree image: {exc})")
