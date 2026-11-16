"""Creating random trees and the initial population.

Every function takes an `rng` (a random.Random instance) so each GP run
draws from its own seeded generator. The default is the global `random`
module, which has the same methods, for quick interactive use.
"""

import random

from .gp_config import DEFAULT_CONFIG
from .primitives import FUNCTIONS


def random_tree(depth, method, terminals, functions=FUNCTIONS,
                terminal_prob=DEFAULT_CONFIG.terminal_prob, rng=random):
    """Generate a random expression tree using the 'full' or 'grow' method.

    full: every branch reaches exactly `depth`.
    grow: each node becomes a terminal early with probability terminal_prob.
    """

    if depth == 0 or (
        method == 'grow'
        and rng.random() < terminal_prob
    ):
        return rng.choice(terminals)

    op = rng.choice(list(functions))
    arity = functions[op][1]

    return (
        op,
        *(random_tree(depth - 1, method, terminals, functions, terminal_prob, rng)
          for _ in range(arity))
    )


def ramped_half_and_half(terminals, functions=FUNCTIONS,
                         config=DEFAULT_CONFIG, rng=random):
    """Generate the initial population using full and grow methods.

    Cycles through every (depth, method) pair, so each depth gets both
    methods whatever the number of depths. (Pairing depth = i % n_depths with
    method = i % 2 gives each depth only one method when n_depths is even.)
    """

    depths = range(config.min_init_depth, config.max_init_depth + 1)
    combos = [(d, m) for d in depths for m in ('full', 'grow')]

    population = []
    for i in range(config.population_size):
        depth, method = combos[i % len(combos)]
        population.append(random_tree(depth, method, terminals, functions,
                                      config.terminal_prob, rng))

    return population
