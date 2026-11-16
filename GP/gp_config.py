"""Default GP run settings.

Named gp_config.py (not config.py) so it is tracked by Git: the root
.gitignore excludes the GA's local config.py override.
"""

POPULATION_SIZE = 200
MAX_GENERATIONS = 50
TOURNAMENT_SIZE = 5
CROSSOVER_RATE = 0.8     # probability an offspring is made by crossover
MUTATION_RATE = 0.1      # probability an offspring is made by mutation
                         # (the remainder is plain reproduction)
ELITISM = 1
MIN_INIT_DEPTH = 2
MAX_INIT_DEPTH = 4
MAX_DEPTH = 8            # bloat control: offspring deeper than this are rejected
MUTATION_SUBTREE_DEPTH = 2
TERMINAL_PROB = 0.3      # chance "grow" stops early at each node
TARGET_FITNESS = 1e-6    # stop when the best error falls below this
SEED = 42
