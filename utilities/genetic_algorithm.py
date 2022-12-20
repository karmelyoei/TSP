# Genetic Algorithm
import random
import math
import matplotlib.pyplot as plt
import geopy.distance

from .visualize import plotTSP

class GeneticAlgorithm():
    def __init__(self,coords):
        self.coords = coords
        self.number_of_cities = len(coords)
        self.nodes = [i for i in range(self.number_of_cities)]
        self.best_fitness = float("Inf")
        self.best_solution = None
        self.size_rate = 2
        self.mutation_rate = 0.6
        self.k = 2
        self.iteration = 2
        self.children = []
        self.offspring = []
        self.fitness_list = []
        self.population = []

    def initial_chromosome(self):
        """
        Greedy algorithm to get an initial chromosome (closest-neighbour).
        """
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.nodes)
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))  # nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return solution, cur_fit

    def generate_population(self, first_chromosome):
        """Generate Population that near the chromosome using mutation"""
        pop_size = len(self.nodes) * self.size_rate
        neighbours = []
        for x in range(pop_size):
            for i in range(len(first_chromosome)):
                if random.randrange(0, 1) < self.mutation_rate:
                    j = random.randint(0,len(first_chromosome) - 1)
                    neighbour = first_chromosome.copy()
                    neighbour[i] = first_chromosome[j]
                    neighbour[j] = first_chromosome[i]
                    neighbours.append(neighbour)
        return neighbours

    def dist(self, node_0, node_1):
        """
        Euclidean distance between two nodes.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        return geopy.distance.geodesic(coord_0, coord_1).km

    def fitness(self, chromosome):
        """
        Total distance of the current solution path.
        """
        cur_fit = 0
        for i in range(self.number_of_cities):
            cur_fit += self.dist(chromosome[i % self.number_of_cities], chromosome[(i + 1) % self.number_of_cities])
        return cur_fit

    def pop_fitness(self):
        """
        Total distance for each chromosome in genetic algorithm
        """
        pop_cost = []
        for chromosome in self.population:
            cost = self.fitness(chromosome)
            pop_cost.append(cost)
        return pop_cost

    # Restricted tournament selection
    def tournament_selection(self):
        """https://www.geeksforgeeks.org/tournament-selection-ga/"""
        parents = []
        random_index = random.randint(0, len(self.population) - 1 )
        selected_chromosome = self.population[random_index]
        selected_cost = self.fitness(selected_chromosome)
        while len(parents) != len(self.population):
            for i in range(0, self.k):
                current_chromosome = self.population[i]
                current_cost = self.fitness(current_chromosome)
                if selected_chromosome is None or current_cost >= selected_cost:
                    selected_chromosome = current_chromosome
                    parents.append(selected_chromosome)

        return parents

    # Ordered Crossover method OX
    def crossover(self,mum, dad):
        """Implements ordered crossover https://stackoverflow.com/questions/50489450/genetic-algorithm-ordered-crossover-in-python"""
        size = len(mum)
        children = []

        # Choose random start/end position for crossover
        child1, child2 = [-1] * size, [-1] * size
        start, end = sorted([random.randrange(size) for _ in range(2)])

        # Replicate mum's sequence for child1, dad's sequence for child2
        alice_inherited = []
        bob_inherited = []
        for i in range(start, end + 1):
            child1[i] = mum[i]
            child2[i] = dad[i]
            alice_inherited.append(mum[i])
            bob_inherited.append(dad[i])

        print(child1, child2)
        # Fill the remaining position with the other parents' entries
        current_dad_position, current_mum_position = 0, 0

        fixed_pos = list(range(start, end + 1))
        i = 0
        while i < size:
            if i in fixed_pos:
                i += 1
                continue

            test_alice = child1[i]
            if test_alice == -1:  # to be filled
                dad_trait = dad[current_dad_position]
                while dad_trait in alice_inherited:
                    current_dad_position += 1
                    dad_trait = dad[current_dad_position]
                child1[i] = dad_trait
                alice_inherited.append(dad_trait)

            # repeat block for child2 and mom
            i += 1

        children.append(child1)
        children.append(child2)
        return children

    def crossover2(self,mum, dad):
        """Implements ordered crossover https://stackoverflow.com/questions/50489450/genetic-algorithm-ordered-crossover-in-python"""
        size = len(mum)
        children = []
        child1 = [-1] * size
        child2 = [-1] * size
        # Get two random numbers
        start = random.randint(0,(size - 2))
        end = random.randint(0,(size - 2))
        # make sure that the start index less than the end
        while start >= end or start != 0:
            start = random.randint(0, (size - 2))
            end = random.randint(0, (size - 2))
        # Copy Elements inside the start and end points from parent1 to child1
        child1[start:end+1] = mum[start:end+1]
        child2[start:end+1] = dad[start:end+1]

        # Fill the remaining position with the other parents' entries
        current_dad_position, current_mum_position = 0, 0
        fixed_pos = list(range(start, end + 1))
        i = 0
        while i < size:
            if i in fixed_pos:
                i += 1
                continue

            test_child1 = child1[i]
            if test_child1 == -1:  # to be filled
                dad_trait = dad[current_dad_position]
                while dad_trait in child1:
                    current_dad_position += 1
                    dad_trait = dad[current_dad_position]
                child1[i] = dad_trait

            test_child2 = child2[i]
            if test_child2 == -1:  # to be filled
                mum_trait = mum[current_dad_position]
                while mum_trait in child2:
                    current_mum_position += 1
                    mum_trait = mum[current_dad_position]
                child2[i] = mum_trait

            # repeat
            i += 1

            children.append(child1)
            children.append(child2)
            return children



    # Reverse Sequence Mutation
    def reverse_sequence_mutation(self, chromosome):
        for a in range(len(chromosome)-2):
            i = random.randint(1, len(chromosome) - 1)
            j = random.randint(1, len(chromosome) - 1)
            if i < j:
                temp = chromosome[j]
                chromosome[j] = chromosome[i]
                chromosome[i] = temp
            else:
                continue

        return chromosome

    def apply(self):
        # initial first chromosome using greedy algorithm
        first_chromosome,first_fitness = self.initial_chromosome()

        # initial population according to the number of cities
        initial_population = self.generate_population(first_chromosome)
        unique_population = []
        [unique_population.append(x) for x in initial_population if x not in unique_population]
        self.population = unique_population
        for gen in range(self.iteration):
            # Clear the prev offspring
            self.offspring = []
            # Selecting the best parents in the population for mating
            parents = self.tournament_selection()
            for i, parent in enumerate(parents):
                if i % 2 == 0:
                    # Generating next generation using crossover.
                    self.children.extend(self.crossover2(parents[i], parents[i+1]))
            # Adding some variations to the offsrping using mutation.
            for child in self.children:
                 self.offspring.append(self.reverse_sequence_mutation(child))
            self.population = self.offspring
        # Evaluate all the chromosomes on the last generation we got and get the min cost ( best evaluation)
        total_eval = self.pop_fitness()
        self.best_fitness = min(total_eval)
        self.best_solution = self.population[total_eval.index(self.best_fitness)]
        return self.best_solution,self.best_fitness

    def visualize_routes(self):
        """
        Visualize the TSP route with matplotlib.
        """
        plotTSP([self.best_solution], self.coords)

    def plot_learning(self):
        """
        Plot the fitness through iterations.
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel("Fitness")
        plt.xlabel("Iteration")
        plt.show()