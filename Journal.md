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
