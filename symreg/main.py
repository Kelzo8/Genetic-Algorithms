"""Run symbolic regression with the GP engine.

From the repository root:  python -m symreg.main
"""

from GP import DEFAULT_CONFIG, genetic_programming

from .fitness import fitness
from .problem import TERMINALS


if __name__ == "__main__":

    # The seed lives in the config (DEFAULT_CONFIG.seed); pass e.g.
    # dataclasses.replace(DEFAULT_CONFIG, seed=7) to change it.
    result = genetic_programming(fitness, TERMINALS, config=DEFAULT_CONFIG)

    print("Final solution:", result.best)

    try:
        from GP.visualisation import visualise_tree
        visualise_tree(result.best, "gp_tree")
    except Exception as exc:  # Graphviz missing or no display available
        print(f"(Skipped tree image: {exc})")
