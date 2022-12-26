# Genetic Algorithm
import random
import logging
import geopy.distance
import copy
import ast

class GeneticAlgorithm():
    def __init__(self,coords):
        self.coords = coords
        self.number_of_cities = len(coords)
        self.nodes = [i for i in range(self.number_of_cities)]
        self.best_fitness = float("Inf")
        self.best_solution = None
        self.size_rate = 2
        self.mutation_rate = 0.6
        self.iteration_prob = {'3':1,'5':1,'10':2,'15':2,'20':2,'50':3,'100':4}
        self.children = []
        self.offspring = []
        self.fitness_list = []
        self.population = []
        self.pop_size = len(self.nodes) * self.size_rate
        self.k = 3

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
        neighbours = []
        while len(neighbours) != self.pop_size:
            for x in range(self.pop_size):
                if random.randrange(0, 1) < self.mutation_rate:
                    j = random.randint(0,len(first_chromosome) - 1)
                    i = random.randint(0, len(first_chromosome) - 1)
                    neighbour = first_chromosome.copy()
                    neighbour[i] = first_chromosome[j]
                    neighbour[j] = first_chromosome[i]
                    neighbours.append(neighbour)
        return neighbours

    def dist(self, node_0, node_1):
        """
        geo distance between two nodes.
        """
        coord_0, coord_1 = (float(self.coords[node_0][0]),float(self.coords[node_0][1])), (float(self.coords[node_1][0]),float(self.coords[node_1][1]))
        distance = geopy.distance.geodesic(coord_0, coord_1).km
        return distance

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
        """Algorithm --
        1.Select k individuals from the population and perform a tournament amongst them
        2.Select the best individual from the k individuals
        3. Repeat process 1 and 2 until you have the desired amount of population"""
        parent_population = copy.deepcopy(self.population)
        offspring_population = []
        for p in range(len(self.population)):
                temp_population = {}
                for j in range(self.k):
                    temp_population[f'{random.choice(parent_population)}'] = self.fitness(random.choice(parent_population))
                # sort solutions by fitness
                temp_population = {k: v for k, v in sorted(temp_population.items(), key=lambda item: item[1])}
                offspring_population.append(ast.literal_eval(next(iter(temp_population))))
        return offspring_population

    # Ordered Crossover method OX
    def crossover(self, mum, dad):
        """Implements ordered crossover"""
        size = len(mum) - 1
        children = []

        # Choose random start/end position for crossover
        start, end = sorted([random.randrange(size) for _ in range(2)])

        # Identify the elements from mum's sequence which end up in alice,
        # and from dad's which end up in bob
        mumxo = set(mum[start:end + 1])
        dadxo = set(dad[start:end + 1])

        # Take the other elements in their original order
        alice = [i for i in dad if not i in mumxo]
        bob = [i for i in mum if not i in dadxo]

        # Insert selected elements of mum's sequence for alice, dad's for bob
        alice[start:start] = mum[start:end + 1]
        bob[start:start] = dad[start:end + 1]

        children.append(alice)
        children.append(bob)

        # Return twins
        return children

    # Reverse Sequence Mutation
    def reverse_sequence_mutation(self, chromosome):
        """Reverse Sequence Mutation """
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
        """Applying the Genetic Algorithm in following steps:
        1- Greedy initial population.
        2- Tournament Parents Selection
        3- Crossover parents
        4  Mutation
        5  Repeat till the last generation
        6  Take the lowest route path distance"""
        # M generation vs fitness
        generation_fitness = []
        # initial first chromosome using greedy algorithm
        first_chromosome,first_fitness = self.initial_chromosome()

        print("Greedy initial solution path,fitness", first_chromosome,first_fitness)

        # initial population according to the number of cities
        initial_population = self.generate_population(first_chromosome)
        unique_population = []
        [unique_population.append(x) for x in initial_population if x not in unique_population]
        self.population = unique_population

        print("population size", len(self.population))
        logging.info(f"First Population {len(self.population)}")

        self.iteration = self.iteration_prob[f'{self.number_of_cities}']
        for gen in range(self.iteration):
            # Clear the prev offspring
            self.offspring = []
            # Selecting the best parents in the population for mating
            parents = self.tournament_selection()
            print("parents length",len(parents))

            for i, parent in enumerate(parents):
                if i % 2 == 0 and i != len(parents)-1:
                    # Generating next generation using crossover.
                    self.children.extend(self.crossover(parents[i], parents[i+1]))
            if len(parents) % 2 != 0 :
                # Add the last chromosome cause it's the only one which didnt crossover
                last = parents[len(parents)-1]
                self.children.extend([last])
            # Adding some variations to the offsrping using mutation.
            for child in self.children:
                 self.offspring.append(self.reverse_sequence_mutation(child))

            self.population = self.offspring
            total_eval = self.pop_fitness()

            logging.info(f"Number of iteration {gen}, lowest path distance{min(total_eval)}")
            generation_fitness.append([gen, min(total_eval)])

        # Evaluate all the chromosomes on the last generation we got and get the min cost ( best evaluation)
        total_eval = self.pop_fitness()
        self.best_fitness = min(total_eval)
        self.best_solution = self.population[total_eval.index(self.best_fitness)]
        return self.best_solution,self.best_fitness,generation_fitness
