import time
import logging
import csv

from utilities import HillClimbing, SimAnneal, GeneticAlgorithm



def main( ):
    # Read data from json file
    cities_data = dict()
    time_executing = {}

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
            cities_world[city_name] = coordinates

    # plotting_world(list(cities_world.values())[:10])

    for number in number_of_cities:
        coor = list(cities_world.values())[:number]
        print("***************************")
        print(f"Starting with {number} of cities with coordination {coor}")
        print("***************************")
        print(f"-----Hill climbing algorithm-----------")

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
        time_executing["hill-climbing-{number}"] = total_time
        print(f" Hill Clim, The best route of {number}  cities is {solution} with total distance {distance} km  took {total_time:0.4f} seconds")

        logging.info("Results from Hill Climbing Algorithm:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {total_time:0.4f}")

        # Implementing Simulated Annealing Algorithm for TSP
        print(
            f"----------Simulated annealing algorithm ---------------")
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

        time_executing["sim-ann-{number}"] = total_time

        print(f"Simulated Anne, The best route of {number}  cities is {solution} with total distance {distance} km. took {total_time:0.4f} seconds")

        logging.info("Results from Simulated annealing algorithm:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {total_time:0.4f}")

        logging.info(f"Starting  Genetic algorithm for {number} cities")
        logging.info(f"Start distance: {coor}")

        print("-----------Genetic Algorithm----------------")
        genetic_algorithm = GeneticAlgorithm(coor)
        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        best_solution, best_fitness = genetic_algorithm.apply()

        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time
        time_executing["genetic-algorithm-{number}"] = total_time

        print(f"GA,The best route of {number}  cities is {best_solution} with total distance {best_fitness} km. took {total_time:0.4f} seconds")

        logging.info("Results from algorithm:")
        logging.info(f"Best Sequence: {best_solution}")
        logging.info(f"Least distance is {best_fitness} km")
        logging.info(f"Time: {total_time:0.4f}")

    # Plotting time VS number of cities

    # Plotting fitness solution evaluation vs iteration
    # GA = generations
    # SA = cooling
    # Hill = iteration
    


if __name__ == "__main__":
    main()
