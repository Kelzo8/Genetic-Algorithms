"""GP run settings.

Every setting lives in one GPConfig object that is passed into
genetic_programming(), so experiments can change any of them per run
(e.g. GPConfig(tournament_size=3)) for parameter sensitivity studies,
without editing this file.

Named gp_config.py (not config.py) so it is tracked by Git: the root
.gitignore excludes the GA's local config.py override.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GPConfig:
    """Parameters for one GP run. frozen=True means a config cannot be
    changed by accident during a run; use dataclasses.replace() to make a
    modified copy."""

    population_size: int = 200
    max_generations: int = 50
    tournament_size: int = 5
    crossover_rate: float = 0.8      # probability an offspring is made by crossover
    mutation_rate: float = 0.1       # probability an offspring is made by mutation
                                     # (the remainder is plain reproduction)
    elitism: int = 1                 # best individuals copied unchanged each generation
    min_init_depth: int = 2
    max_init_depth: int = 4
    max_depth: int = 8               # bloat control: offspring deeper than this are rejected
    mutation_subtree_depth: int = 2  # depth of the new subtree inserted by mutation
    terminal_prob: float = 0.3       # chance "grow" stops early at each node
    target_fitness: float | None = 1e-6  # stop when best fitness < this; None = full budget
    cache_fitness: bool = True       # reuse the fitness of trees seen before; only valid
                                     # if fitness_fn is deterministic (same tree -> same value)
    seed: int = 42

    def __post_init__(self):
        """Reject settings that would silently break a run."""
        if not 0 <= self.crossover_rate + self.mutation_rate <= 1:
            raise ValueError("crossover_rate + mutation_rate must be in [0, 1]")
        if not 1 <= self.tournament_size <= self.population_size:
            raise ValueError("tournament_size must be between 1 and population_size")
        if not 0 <= self.elitism < self.population_size:
            raise ValueError("elitism must be less than population_size")
        if not 0 <= self.min_init_depth <= self.max_init_depth <= self.max_depth:
            raise ValueError("need min_init_depth <= max_init_depth <= max_depth")


DEFAULT_CONFIG = GPConfig()
