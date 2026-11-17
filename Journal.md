# Genetic Algorithms Journal

- **Student Names:** [James Kelly] [Andrew Jaffray]
- **Student ID:** [23370858] [23382163]

# Week 1 — 6/11/26

Designed and implemented a genetic algorithm for OneMax. Got familiar with the main ideas: fitness, selection, crossover and mutation etc. We also began talking about some possible ideas for the project and how it might be structured

Genetic Algorithms:
![GA population on a fitness landscape: spread out exploring at generation 0, converged on the optima by generation 40](images/ga_population_on_fitness_landscape.png)

The picture above is the mental model to hold on to. Think of every possible solution as a point on a landscape, where height is fitness. At the start, the population is scattered all over it. Over the generations, selection pulls individuals uphill. Crossover and mutation keep sending out “probes” to nearby and in-between points. The population behaves like a swarm feeling its way up the landscape.

## Differences between GA and GP

- Representation: GA uses a string, GP uses a tree.
- Crossover: GA swaps parts of strings, GP swaps subtrees.
- Mutation: GA changes parts of a string, GP changes parts of a tree.
- Fitness: GA scores a string GP runs a tree as a program and scores its output.

- Used Graphviz for visualising the tree to see the terminals and operators

## Testing our GP
- Our GP did quite well with the first set of data, achieving perfect fitness within 3 generations. However it never achieved perfect fitness for second set of data. We tried changing the numerous variables such as generation, population etc. to achieve a lower MAE but it still wasn't enough to get to the correct formula fully.

## Project Comparison: Flappy Bird vs Pac-Man
## Overview

| | Flappy Bird | Pac-Man |
|---|---|---|
| What GP evolves | Flap or not (one output) | 1 of 4 directions |
| Primitive set | Small, all numeric (`dy`, `velocity`, `dx`, gap edges, constants) | Larger (distances to pills, power pills, ghosts, edible ghosts, pills left, constants) |
| Functions | `+ − ×`, protected `/`, `if_less_than`, `max`, `min` | Same, plus more conditionals |
| Fitness | Frames survived + bonus per pipe, averaged over 3–5 seeds | Game score (+ survival bonus), averaged over 3–5 games |
| Typical evolved solution | Small feedback rule, e.g. `(dy + velocity × 2) − 5` | Larger trees balancing pill collection and ghost avoidance |

## Ways to extend

| Flappy Bird | Pac-Man |
|---|---|
| Harder variants: narrower gaps, moving pipes, increasing speed | Test on unseen mazes |
| Generalisation: train easy, test hard | Co-evolve ghosts as a second population |
| GP vs GE on the same controller | GP vs GE on the same controller |


## Idea: GP for the Travelling Salesman Problem — evolve a heuristic. Not evolving a tour

### Concept
- A TSP solution is an ordering of cities, which suits a GA better than GP. 
Evolving one tour also only solves one map.

- Instead, we will use GP to evolve a **rule for building tours** that works on any map. 

At each step, the evolved tree scores every unvisited city and the tour moves to the best one. The tree's inputs are simple facts about each candidate city, such as its distance from the current city and from the remaining cities.

The simplest possible rule, "go to the nearest city", is the classic nearest-neighbour heuristic. Our goal is to see whether GP can evolve something better.

### Research question
Can GP evolve a heuristic that beats nearest neighbour and still works on larger maps it has never seen?

## Decision: fixed training set 

We score every tree on the same set of training maps for the whole run, instead of new maps each generation.

- Same maps means fitness values are directly comparable and deterministic, so we can cache them and the convergence curves are clean.

# 17/11/26 — Presentation and Research

## Research influencing our design
- Reviewed Koza’s *Genetic Programming* manuscript [1]. This supports our proposed expression-tree representation, subtree crossover and subtree mutation. It also informed our use of protected division to handle division by zero.
- Reviewed Ryan and Azad’s *Sensible Initialisation in Chorus* [2]. This strengthened our rationale for combining Full and Grow across different depths to encourage varied initial tree structures.
- Recognised that the Chorus findings do not directly establish what will work best for our TSP system. We chose ramped half-and-half to encourage structural variety, not because it guarantees better performance.

## Presentation and documentation decisions
- Prepared short speaker-note bullets explaining the representation, operators and initialisation.
- Chose IEEE numbered referencing and began building the reference list using sources we have reviewed.
- Changed our project idea from evolving a Flappy Bird controller to evolving a TSP tour-construction heuristic. The TSP project gives us a clearer way to compare against a simple baseline (nearest neighbour) and investigate generalisation on unseen maps and larger instances.

## References Added
[1] J. R. Koza, “Genetic programming,” manuscript submitted for the *Encyclopedia of Computer Science and Technology*, ver. 2, Aug. 18, 1997.

[2] C. Ryan and R. M. A. Azad, “Sensible initialisation in Chorus,” in *Proc. European Conf. Genetic Programming (EuroGP)*, Lecture Notes in Computer Science, vol. 2610, 2003, pp. 394–403.