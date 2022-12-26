import time
import logging
import gc
from memory_profiler import profile
from utilities import HillClimbing, time_plot, plotting_route, convergance_plot
from get_cities import get_capital_cities_coor
import datetime

@profile
def main(cities_world):
    """Run the Hill Climb Algorithm for TSP"""
    # Number of Cities
    # N = 3, 5, 10, 15, 20, 50, 100
    number_of_cities = [3, 5, 10, 15, 20, 50, 100]

    # Track Time and Convergence over iteration
    time_executing = {}
    solutions_fitness_cities = {}

    # Configure the logging
    logging.basicConfig(filename='results_HC/hillClimbAlgo_log1',
                        level=logging.INFO,
                        format='%(asctime)s\t\t%(message)s',
                        filemode='a')

    for number in number_of_cities:
        coor = list(cities_world.values())[:number]

        print(f"-----Hill climbing algorithm-----------")
        print("***************************")
        print(f"Starting with {number} of cities")
        print("***************************")
        logging.info(f"Starting Hill Climbing algorithm for {number} cities")

        # Initialize the Class object of Hill Climbing Algorithm
        hill_climb_algorithm = HillClimbing(coor)

        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        # Get the best Solution with the route Length
        solution, distance, iteration_fitness = hill_climb_algorithm.apply()
        solutions_fitness_cities[f"{number}"] = [solution, distance, iteration_fitness]

        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time
        time_executing[f"{number}"] = total_time

        print(
            f" Hill Clim, The best route for {number}  cities is {solution} with total distance {distance} km  took {total_time:0.4f} seconds")

        # Plotting route
        plotting_route(cities_world, solution, distance, "HC")

        logging.info("Results:")
        logging.info(f"Best Sequence: {solution}")
        logging.info(f"Least distance is {distance} km")
        logging.info(f"Time: {str(datetime.timedelta(seconds=total_time))} seconds")

        gc.collect()

    return time_executing, solutions_fitness_cities


if __name__ == "__main__":

    # Get the world Capitals
    cities_world = get_capital_cities_coor()
    time_executing, solutions_fitness_cities = main(cities_world)

    # Plot Big O for time
    time_plot(time_executing, algorithm_name='HC')

    # Plot Convergence Fitness value vs generation
    # [best_solution,best_fitness,generation_fitness]
    # [gen, min(total_eval)]
    convergance_plot(solutions_fitness_cities, "HC")
