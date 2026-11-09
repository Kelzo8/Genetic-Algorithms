# GA Flow

1. Create a random population of binary strings.
2. Count the 1s in each string to get its fitness.
3. Record the best and average fitness.
4. Stop if the best string is all 1s or the generation limit is reached.
5. Copy the best individual to the next population.
6. Select parents with tournament selection. (The highest fitness from a population becomes a parent)
7. Apply crossover and mutation to make children.
8. Fill the next population with the children.
9. Repeat from step 2.
