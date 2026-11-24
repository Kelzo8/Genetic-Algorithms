from GP.algorithm import genetic_programming
from GP.gp_config import GPConfig
from GP.primitives import FUNCTIONS
from GP.tree import to_string

from .baselines import nearest_neighbour_tour
from .constructor import construct_tour
from .datasets import generate_uniform_map
from .fitness import make_fitness_function


def main() -> None:
    """Generate the single pilot instance, evolve a rule and report results."""
    instance = generate_uniform_map(n_cities=20, seed=42)
    terminals = ["D_cn", "D_in", "D_c"]
    fitness = make_fitness_function([instance], terminals, FUNCTIONS)
    config = GPConfig(
        population_size=20,
        max_generations=5,
        seed=42,
        target_fitness=None,
    )

    result = genetic_programming(
        fitness,
        terminals,
        FUNCTIONS,
        config=config,
        verbose=False,
    )

    gp_tour = construct_tour(result.best, instance, terminals, FUNCTIONS)
    gp_length = instance.tour_length(gp_tour)
    nn_tour = nearest_neighbour_tour(instance)
    nn_length = instance.tour_length(nn_tour)
    ratio = gp_length / nn_length if nn_length > 0.0 else float("inf")

    print(f"Best evolved rule: {to_string(result.best)}")
    print(f"GP tour: {gp_tour}")
    print(f"GP tour length: {gp_length:.6f}")
    print(f"Nearest-neighbour tour: {nn_tour}")
    print(f"Nearest-neighbour tour length: {nn_length:.6f}")
    print(f"GP/NN ratio: {ratio:.6f}")
    print(f"GP beat nearest neighbour: {gp_length < nn_length}")


if __name__ == "__main__":
    main()
