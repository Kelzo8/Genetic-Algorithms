import random

from config import SEED
from visualisation import visualise_tree
from algorithm import genetic_programming


if __name__ == "__main__":

    random.seed(SEED)

    best = genetic_programming()

    print("Final solution:", best)
    visualise_tree(best, "gp_tree")