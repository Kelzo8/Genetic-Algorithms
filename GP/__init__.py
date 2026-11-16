"""Problem-independent genetic programming engine.

A problem supplies a terminal list and a fitness function (lower is better)
and calls genetic_programming(). See symreg/ for a complete example.
"""

from .algorithm import GPResult, genetic_programming
from .gp_config import DEFAULT_CONFIG, GPConfig
from .primitives import FUNCTIONS

__all__ = ["DEFAULT_CONFIG", "FUNCTIONS", "GPConfig", "GPResult",
           "genetic_programming"]
