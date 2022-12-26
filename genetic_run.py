import time
import gc
import logging
import tracemalloc
import datetime
from memory_profiler import profile
from utilities import GeneticAlgorithm, time_plot,map_world_plt,convergance_plot,plotting_route
from get_cities import get_capital_cities_coor

@profile
def main(cities_world):
    # check memeory leak
    tracemalloc.start()

    # Configure the logging
    logging.basicConfig(filename='results_GA/GA_log',
                        level=logging.INFO,
                        format='%(asctime)s\t\t%(message)s',
                        filemode='a')

    # Number of Cities
    # N = 3, 5, 10, 15, 20, 50, 100
    number_of_cities = [3,5,10,15,20,50,100]

    # plotting_world(list(cities_world.values())[:10])
    # Time consumed VS number of cisites
    time_cities = {}
    solutions_fitness_cities = {}

    for number in number_of_cities:
        coor = list(cities_world.values())[:number]

        print("-----------Genetic Algorithm----------------")
        print(f"Starting with Genetic Algorithm {number} of cities")
        logging.info(f"Starting  Genetic Algorithm for {number} cities")

        genetic_algorithm = GeneticAlgorithm(coor)
        # Start monitoring time before the algorithm
        start_time = time.perf_counter()

        best_solution, best_fitness,generation_fitness = genetic_algorithm.apply()
        solutions_fitness_cities[f'{number}'] = [best_solution,best_fitness,generation_fitness]

        # After applying the Algorithm
        end_time = time.perf_counter()
        total_time = end_time - start_time
        time_cities[f'{number}'] = total_time

        print(f"GA,The best route of {number}  cities is {best_solution} with total distance {best_fitness} km. took {total_time:0.4f} seconds")
        # Plotting route
        plotting_route(cities_world, best_solution, best_fitness, "GA")

        logging.info("Results:")
        logging.info(f"Best Sequence: {best_solution}")
        logging.info(f"Least distance is {best_fitness} km")
        logging.info(f"Time: {str(datetime.timedelta(seconds=total_time))}")

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('traceback')

        #pick the biggest memory block
        stat = top_stats[0]
        print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
        for line in stat.traceback.format():
            print(line)

        gc.collect()

        # Draw map with coordinates and link them together write total distance
        # map_world_plt(number, cities_world)

    return time_cities,solutions_fitness_cities

if __name__ == "__main__":
    # managing the garbage
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)

    # Get the world Capitals
    cities_world = get_capital_cities_coor()
    time_cities,solutions_fitness_cities = main(cities_world)

    # Plot Big O for time
    time_plot(time_cities,algorithm_name='GA')


    #Plot Convergance Fitness value vs generation
    convergance_plot(solutions_fitness_cities,"GA")



