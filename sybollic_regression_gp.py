"""
A basic genetic programming (GP) example: symbolic regression.

Goal: given only sample points (x, y), evolve a *program* (a mathematical
expression) that reproduces them. The hidden target function is

    f(x) = x^2 + x + 1

but the algorithm never sees this formula, only its outputs.
"""

import math
import operator
import random

# ---- Parameters ----
POPULATION_SIZE = 200
MAX_GENERATIONS = 50
TOURNAMENT_SIZE = 5
CROSSOVER_RATE = 0.8     # probability an offspring is made by crossover
MUTATION_RATE = 0.1      # probability an offspring is made by mutation
                         # (the remainder is plain reproduction)
ELITISM = 1
MIN_INIT_DEPTH = 2
MAX_INIT_DEPTH = 4
MAX_DEPTH = 8            # bloat control limit
TERMINAL_PROB = 0.3      # chance "grow" stops early at each node
SEED = 42


# ---- Problem definition ----
def target(x):
    return x * x + x + 1


SAMPLE_POINTS = [i / 10 for i in range(-10, 11)]  # x = -1.0, -0.9, ..., 1.0


# ---- Primitive set ----
def protected_div(a, b):
    return a / b if abs(b) > 1e-6 else 1.0


FUNCTIONS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': protected_div,
}
TERMINALS = ['x', 1, 2]


# ---- Tree representation ----
# A tree is either a terminal ('x' or a number) or a tuple (op, left, right).
def random_tree(depth, method):
    """Build a random tree using the 'full' or 'grow' method."""
    if depth == 0 or (method == 'grow' and random.random() < TERMINAL_PROB):
        return random.choice(TERMINALS)
    op = random.choice(list(FUNCTIONS))
    return (op, random_tree(depth - 1, method), random_tree(depth - 1, method))


def evaluate(tree, x):
    if isinstance(tree, tuple):
        op, left, right = tree
        return FUNCTIONS[op](evaluate(left, x), evaluate(right, x))
    return x if tree == 'x' else tree


def depth(tree):
    if isinstance(tree, tuple):
        return 1 + max(depth(tree[1]), depth(tree[2]))
    return 0


def size(tree):
    if isinstance(tree, tuple):
        return 1 + size(tree[1]) + size(tree[2])
    return 1


def to_string(tree):
    if isinstance(tree, tuple):
        op, left, right = tree
        return f"({to_string(left)} {op} {to_string(right)})"
    return str(tree)


# ---- Subtree helpers (used by crossover and mutation) ----
# A node is addressed by its path from the root: () is the root, (1,) is the
# root's left child, (1, 2) is that child's right child, and so on.
def node_paths(tree, path=()):
    yield path
    if isinstance(tree, tuple):
        yield from node_paths(tree[1], path + (1,))
        yield from node_paths(tree[2], path + (2,))


def get_subtree(tree, path):
    for index in path:
        tree = tree[index]
    return tree


def replace_subtree(tree, path, new_subtree):
    if not path:
        return new_subtree
    node = list(tree)
    node[path[0]] = replace_subtree(tree[path[0]], path[1:], new_subtree)
    return tuple(node)


# ---- Fitness ----
def fitness(tree):
    """Mean absolute error over the sample points (lower is better)."""
    try:
        error = sum(abs(evaluate(tree, x) - target(x)) for x in SAMPLE_POINTS)
    except OverflowError:
        return math.inf
    return error / len(SAMPLE_POINTS) if math.isfinite(error) else math.inf


# ---- Initialisation ----
def ramped_half_and_half():
    population = []
    depths = range(MIN_INIT_DEPTH, MAX_INIT_DEPTH + 1)
    for i in range(POPULATION_SIZE):
        d = depths[i % len(depths)]
        method = 'full' if i % 2 == 0 else 'grow'
        population.append(random_tree(d, method))
    return population


# ---- Selection ----
def tournament_selection(population, fitnesses, k=TOURNAMENT_SIZE):
    """Pick k individuals at random and return the one with the lowest error."""
    contestants = random.sample(range(len(population)), k)
    winner = min(contestants, key=lambda i: fitnesses[i])
    return population[winner]


# ---- Variation operators ----
def subtree_crossover(parent1, parent2):
    """Replace a random subtree of parent1 with a random subtree of parent2."""
    point1 = random.choice(list(node_paths(parent1)))
    point2 = random.choice(list(node_paths(parent2)))
    child = replace_subtree(parent1, point1, get_subtree(parent2, point2))
    return child if depth(child) <= MAX_DEPTH else parent1


def subtree_mutation(parent):
    """Replace a random subtree with a freshly grown random tree."""
    point = random.choice(list(node_paths(parent)))
    child = replace_subtree(parent, point, random_tree(2, 'grow'))
    return child if depth(child) <= MAX_DEPTH else parent


# ---- Main loop ----
def genetic_programming():
    population = ramped_half_and_half()

    for generation in range(MAX_GENERATIONS):
        fitnesses = [fitness(tree) for tree in population]

        best_idx = min(range(POPULATION_SIZE), key=lambda i: fitnesses[i])
        best = population[best_idx]
        avg_size = sum(size(tree) for tree in population) / POPULATION_SIZE
        print(f"Gen {generation:2d} | error = {fitnesses[best_idx]:.4f} | "
              f"avg size = {avg_size:5.1f} | {to_string(best)}")

        if fitnesses[best_idx] < 1e-9:
            print(f"\nPerfect program found in generation {generation}:")
            print(f"  {to_string(best)}")
            return best

        # Elitism: carry the best programs straight into the next generation
        ranked = sorted(range(POPULATION_SIZE), key=lambda i: fitnesses[i])
        next_population = [population[i] for i in ranked[:ELITISM]]

        # Fill the rest with offspring
        while len(next_population) < POPULATION_SIZE:
            r = random.random()
            parent = tournament_selection(population, fitnesses)
            if r < CROSSOVER_RATE:
                other = tournament_selection(population, fitnesses)
                child = subtree_crossover(parent, other)
            elif r < CROSSOVER_RATE + MUTATION_RATE:
                child = subtree_mutation(parent)
            else:
                child = parent
            next_population.append(child)

        population = next_population

    best = min(population, key=fitness)
    print("\nReached the generation limit. Best program:")
    print(f"  {to_string(best)}  (error = {fitness(best):.4f})")
    return best


if __name__ == "__main__":
    random.seed(SEED)
    genetic_programming()
