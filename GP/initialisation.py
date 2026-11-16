import random
from gp_config import POPULATION_SIZE, MIN_INIT_DEPTH, MAX_INIT_DEPTH, TERMINAL_PROB
from primitives import FUNCTIONS


def random_tree(depth, method, terminals, functions=FUNCTIONS):
    """Generate a random expression tree using the 'full' or 'grow' method."""

    if depth == 0 or (
        method == 'grow'
        and random.random() < TERMINAL_PROB
    ):
        return random.choice(terminals)

    op = random.choice(list(functions))
    arity = functions[op][1]

    return (
        op,
        *(random_tree(depth - 1, method, terminals, functions) for _ in range(arity))
    )


def ramped_half_and_half(terminals, functions=FUNCTIONS,
                         population_size=POPULATION_SIZE):
    """Generate the initial population using full and grow methods.

    Cycles through every (depth, method) pair, so each depth gets both
    methods whatever the number of depths. (Pairing depth = i % n_depths with
    method = i % 2 gives each depth only one method when n_depths is even.)
    """

    depths = range(MIN_INIT_DEPTH, MAX_INIT_DEPTH + 1)
    combos = [(d, m) for d in depths for m in ('full', 'grow')]

    population = []
    for i in range(population_size):
        depth, method = combos[i % len(combos)]
        population.append(random_tree(depth, method, terminals, functions))

    return population
