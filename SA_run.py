import time
import logging
import gc
import datetime
from memory_profiler import profile
from utilities import SimAnneal,time_plot,convergance_plot,plotting_route
from get_cities import get_capital_cities_coor

@profile
def main(cities_world):
    # Number of Cities
    # N = 3, 5, 10, 15, 20, 50, 100
    number_of_cities = [3, 5, 10, 15, 20, 50, 100]

    # Track Time and Convergence over iteration
    time_executing = {}
    solutions_fitness_cities = {}

    # Configure the logging
    logging.basicConfig(filename='results_SA/SA_log',
                        level=logging.INFO,
                        format='%(asctime)s\t\t%(message)s',
                        filemode='a')

    for number in number_of_cities:
        coor = list(cities_world.values())[:number]
        print(f"----------Simulated annealing algorithm ---------------")
        print("***************************")
        logging.info(f"Starting  Simulated annealing algorithm for {number} cities")

        # Initialize the Class object of Hill Climbing Algorithm
        sim_annealing_algorithm = SimAnneal(coor, stopping_iter=number)

        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        solution, distance,iteration_fitness = sim_annealing_algorithm.anneal()
        solutions_fitness_cities[f'{number}'] = [solution, distance, iteration_fitness]
        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time

        time_executing[f"{number}"] = total_time

        print(f"Simulated Anne, The best route of {number}  cities is {solution} with total distance {distance} km. took {total_time:0.4f} seconds")

        # Plotting route
        plotting_route(cities_world, solution, distance, "SA")

        logging.info("Results from Simulated annealing algorithm:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {str(datetime.timedelta(seconds=total_time))}")

        gc.collect()

    return time_executing,solutions_fitness_cities


if __name__ == "__main__":
    # Get the world Capitals
    cities_world = get_capital_cities_coor()
    time_executing, solutions_fitness_cities = main(cities_world)

    # Plot Big O for time
    time_plot(time_executing, algorithm_name='SA')

    # Plot Convergance Fitness value vs generation
    convergance_plot(solutions_fitness_cities,"SA")

