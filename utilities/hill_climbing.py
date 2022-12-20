# Hill Climbing Algorithm
import random
import geopy.distance
import matplotlib.pyplot as plt
from .visualize import plotTSP

class HillClimbing():
    def __init__(self, coords):
        self.coords = coords
        self.number_cities = len(coords)
        self.nodes = [i for i in range(self.number_cities)]
        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []

    # Start the Algorithm by choose a random solution
    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
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

    # Calculate the length of the chosen route
    def dist(self, node_0, node_1):
        """
        Geo distance between two nodes.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        return geopy.distance.geodesic(coord_0, coord_1).km

    def fitness(self, solution):
        """
        Total distance of the current solution path.
        """
        cur_fit = 0
        for i in range(self.number_cities):
            cur_fit += self.dist(solution[i % self.number_cities], solution[(i + 1) % self.number_cities])
        return cur_fit

    # Get the Neighbours of the current Solution
    @staticmethod
    def get_neighbours(solution):
        neighbours = []
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                neighbour = solution.copy()
                neighbour[i] = solution[j]
                neighbour[j] = solution[i]
                neighbours.append(neighbour)
        return neighbours

    # Get the best neighbour
    def get_best_neighbour(self, neighbours):
        best_route_length = self.fitness(neighbours[0])
        best_neighbour = neighbours[0]
        for neighbour in neighbours:
            current_route_length = self.fitness(neighbour)
            if current_route_length < best_route_length:
                best_route_length = current_route_length
                best_neighbour = neighbour
        return best_neighbour, best_route_length

    # Apply the Hill Climbing algorithm over a set of cities
    def apply(self):
        current_solution, current_solution_fitness = self.initial_solution()
        neighbours = self.get_neighbours(current_solution)
        best_neighbour, best_neighbour_route_length = self.get_best_neighbour(neighbours)

        while best_neighbour_route_length < current_solution_fitness:
            current_solution = best_neighbour
            current_solution_fitness = best_neighbour_route_length
            neighbours = self.get_neighbours(current_solution)
            best_neighbour, best_neighbour_route_length = self.get_best_neighbour(neighbours)

        return best_neighbour,best_neighbour_route_length

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
