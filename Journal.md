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

# 22/11/26 — Refining the Research Question and Literature Review

## Change to the research question
- Our earlier question (can GP beat nearest neighbour and work on larger unseen maps?) was too broad to test cleanly.
- Following the lecturer's advice to check the literature first, we narrowed it to one controlled factor:
  **Does training on a mixture of uniform and clustered maps improve the generalisation of GP-evolved TSP construction heuristics to larger, unseen instances, compared with training on uniform maps alone?**
- We are not claiming GP for TSP is new. Our contribution is a controlled study of training-layout diversity.


# 23/11/26 — Locking the project design

## Selected reference method

- We selected Gil-Gala et al. (2023) as our primary reference method.
- We will re-implement their individual-rule GP method, not their ensemble methods.
- Each GP individual is an expression tree that assigns a priority score to an unvisited candidate city.
- During route construction, the candidate with the highest priority is selected, marked visited, and the features are recomputed.
- This produces a valid TSP tour by construction and allows the same rule to be applied to unseen maps.

## Terminal and fitness design

- We will use Gil-Gala et al.’s three features: distance from the current city to the candidate, distance from the start city to the candidate, and distance from the current city to the centroid of the remaining cities.
- We will also include numeric constants.
- We will use Gil-Gala et al.’s original fitness function: the inverse of the mean tour length across the training maps.
- Lower fitness is better because a shorter average training tour gives a larger denominator and therefore a smaller fitness value.
- Nearest neighbour will be used only as an evaluation baseline, not in the training fitness function.

## Controlled experiment

- Our main comparison is uniform-only training versus mixed uniform–clustered training.
- Condition A will use 10 uniform training maps.
- Condition B will use 5 uniform and 5 clustered training maps.
- Both conditions will use the same city-count distribution, GP settings, computational budget, validation maps and test maps.
- Training maps will contain 20–50 cities.
- We will evaluate selected rules on unseen uniform and clustered maps with 50, 100 and 200 cities, as well as selected TSPLIB instances.
- Nearest neighbour and nearest insertion will be used as baselines.

## Validation and reproducibility

- We will use separate validation maps to select the final rule from each independent GP run.
- Test maps will never be used to select rules, tune parameters or choose features.
- We will record seeds and configurations to make results reproducible.
- We will run at least 30 independent runs per condition.

## Presentation updates

- Updated the presentation to match the locked project design.
- Corrected the route-construction rule so that the highest-priority candidate is selected.
- Removed outdated references to additional terminals.
- Added speaker notes matching the current representation, evolutionary process and experimental design.
- Remaining tasks: resolve the stated number of runs, complete references and verify implementation-specific claims.
