import random
from config import POPULATION_SIZE, MIN_INIT_DEPTH, MAX_INIT_DEPTH, TERMINAL_PROB
from primitives import FUNCTIONS, TERMINALS


def random_tree(depth, method):
    """Generate a random expression tree."""

    if depth == 0 or (
        method == 'grow'
        and random.random() < TERMINAL_PROB
    ):
        return random.choice(TERMINALS)

    op = random.choice(list(FUNCTIONS))
    arity = FUNCTIONS[op][1]

    return (
        op,
        *(random_tree(depth - 1, method) for _ in range(arity))
    )


def ramped_half_and_half():
    """Generate the initial population using full and grow methods."""

    population = []
    depths = range(MIN_INIT_DEPTH, MAX_INIT_DEPTH + 1)

    for i in range(POPULATION_SIZE):
        depth = depths[i % len(depths)]
        method = 'full' if i % 2 == 0 else 'grow'

        population.append(random_tree(depth, method))

    return population