import time
import logging
import csv
from matplotlib import pyplot as plt
from utilities import HillClimbing, SimAnneal, GeneticAlgorithm


def plotting_coord(coord):
    for coor in coord:
        x,y = coor[0], coor[1]
        # Plotting
        plt.plot(x, y, 'bo')
        # Displaying grid
        plt.grid()
        # Controlling axis
        plt.axis([-8, 8, -8, 8])
        # Adding title
        plt.title(f'Number of Cities {len(coord)}')
        # Displaying plot
        plt.save(f"{len(coord)}cities.jpg")

def main( ):
    # Read data from json file
    cities_data = dict()

    # Configure the logging
    logging.basicConfig(filename='./results/log',
                        level=logging.INFO,
                        format='%(asctime)s\t\t%(message)s',
                        filemode='w')

    # Number of Cities
    # N = 3, 5, 10, 15, 20, 50, 100
    number_of_cities = [3,5,10,15,20,50,100]

    # Getting the World cities coordination from the file
    cities_world = {}
    with open("./data/worldcities.csv") as file:
        csvreader = csv.reader(file)
        for i,row in enumerate(csvreader):
            if i == 0:
                continue
            coordinates = [row[2],row[3]]
            city_name = row[0]
            cities_world.update({city_name:coordinates})

    for number in number_of_cities:
        keys = list(cities_world.keys())[:3]
        coor = [cities_world[x] for x in keys]

        print(f"Starting hill climbing algorithm for {number} cities with distance{coor}")
        logging.info(f"Starting hill climbing algorithm for {number} cities")
        logging.info(f"Start distance: {coor}")

        # Initialize the Class object of Hill Climbing Algorithm
        hill_climb_algorithm = HillClimbing(coor)
        # Start monitoring time before the algorithm
        start_time = time.perf_counter()
        # Get the best Solution with the route Length
        solution, distance = hill_climb_algorithm.apply()
        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time
        hill_climb_algorithm.visualize_routes()
        hill_climb_algorithm.plot_learning()

        print(f"The best route of {number}  cities is {solution} with total distance {distance} km")
        print(f"The Algorithm took {total_time:0.4f} seconds")

        logging.info("Results from Hill Climbing Algorithm:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {total_time:0.4f}")

        # Implementing Simulated Annealing Algorithm for TSP
        print(
            f"Starting  Simulated annealing algorithm for {number} cities with distance{coor}")
        logging.info(f"Starting  Simulated annealing algorithm for {number} cities")
        logging.info(f"Start distance: {coor}")

        # Initialize the Class object of Hill Climbing Algorithm
        sim_annealing_algorithm = SimAnneal(coor,stopping_iter=number)

        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        solution, distance = sim_annealing_algorithm.anneal()
        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time

        sim_annealing_algorithm.visualize_routes()
        sim_annealing_algorithm.plot_learning()

        print(f"The best route of {number}  cities is {solution} with total distance {distance} km")
        print(f"The Algorithm took {total_time:0.4f} seconds")

        logging.info("Results from Simulated annealing algorithm:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {total_time:0.4f}")

        logging.info(f"Starting  Genetic algorithm for {number} cities")
        logging.info(f"Start distance: {coor}")

        genetic_algorithm = GeneticAlgorithm(coor)
        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        best_solution, best_fitness = genetic_algorithm.apply()

        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time

        sim_annealing_algorithm.visualize_routes()
        sim_annealing_algorithm.plot_learning()

        print(f"The best route of {number}  cities is {best_solution} with total distance {best_fitness} km")
        print(f"The Algorithm took {total_time:0.4f} seconds")

        logging.info("Results from algorithm:")
        logging.info(f"Best Sequence: {best_solution}")
        logging.info(f"Least distance is {best_fitness} km")
        logging.info(f"Time: {total_time:0.4f}")

        plotting_coord(coor)


if __name__ == "__main__":
    main()
