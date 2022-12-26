import geopandas as gpd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import ast

def map_world_plt(number, cities_world):
    coordination = list(cities_world.values())[:number]
    cities_names = list(cities_world.keys())[:number]
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, \
                llcrnrlon=-180, urcrnrlon=180, resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF')
    m.drawmapboundary(fill_color='#FFFFFF')

    for (x, y), city_name in zip(coordination,cities_names):
        lat, lon = x,y
        x, y = m(float(lon), float(lat))
        plt.plot(x, y, 'ok', markersize=10)
        plt.text(x + 2, y,city_name,color="red", fontsize=12)

    plt.title(f"TSP Around the World with {number} of cities")
    plt.savefig(f"/home/karmel/PycharmProjects/TSP_Hill_and_Simulated_algorithms/results/GA_{number}.jpg")
    plt.show()


def time_plot(time_cities,algorithm_name):
    fig_time, ax_time = plt.subplots()
    # make up some data
    times = list(time_cities.values())
    y = times
    x = list(time_cities.keys())
    # plot
    plt.title(f'{algorithm_name}.Time Execute')
    plt.plot(x, y, markersize=20,label=algorithm_name)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.xlabel("Number of Cities")
    plt.ylabel("Time Consumed")
    fig_time.savefig(f"/home/karmel/PycharmProjects/TSP_Hill_and_Simulated_algorithms/results/{algorithm_name}_time_consumed.png")



def plotting_coord(coord):
    for coor in coord:
        x, y = coor[0], coor[1]
        # Plotting
        plt.plot(x, y, 'bo')
        # Displaying grid
        plt.grid()
        # Controlling axis
        plt.axis([-8, 8, -8, 8])
        # Adding title
        plt.title(f'Number of Cities {len(coord)}')
        # Displaying plot
        plt.savefig(f"{len(coord)}cities.jpg")


def plotting_world(world_cities):
    # Creating axes and plotting world map
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    fig, ax = plt.subplots(figsize=(12, 6))
    worldmap.plot(color="#04BAE3", ax=ax)

    for key,value in world_cities.items():
        # Plotting our Impact Energy data with a color map
        x = value[0]
        y = value[1]
        plt.scatter(float(x), float(y), s=20, c='blue', alpha=0.6, vmin=0, vmax=20,
                    cmap='autumn')
        plt.text(float(x) + 2, float(y), key, color="red", fontsize=8)

    # Creating axis limits and title
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])

    plt.title("TSP WorldCities")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")



def plotting_route(world_cities,route, distance,algorithm_name):
    positions = list(world_cities.values())
    N = len(route)
    X = [ast.literal_eval(value[0]) for value in positions][:N]
    Y = [ast.literal_eval(value[1]) for value in positions][:N]

    fig, ax = plt.subplots(2, sharex=True, sharey=True)# Prepare 2 plots

    ax[0].set_title('Raw nodes')
    ax[1].set_title('Optimized tour')

    for key,value in list(world_cities.items())[:N]:
        # Plotting our Impact Energy data with a color map
        x = value[0]
        y = value[1]
        ax[0].scatter(ast.literal_eval(x), ast.literal_eval(y), s=20, c='blue', alpha=0.6, vmin=0, vmax=20,
                    cmap='autumn')
        ax[0].text(ast.literal_eval(x) + 0.2, ast.literal_eval(y), key, color="red", fontsize=8)

        ax[1].scatter(ast.literal_eval(x), ast.literal_eval(y), s=20, c='blue', alpha=0.6, vmin=0, vmax=20,
                      cmap='autumn')
        ax[1].text(ast.literal_eval(x) + 0.2, ast.literal_eval(y), key, color="red", fontsize=8)

    for i in range(len(route)):
        if i == len(route) - 1:
            x = X[route[i]]
            y = Y[route[i]]
            ax[1].annotate("",
                           xy=(x,y), xycoords='data',
                           xytext=(X[route[0]], Y[route[0]]), textcoords='data',
                           arrowprops=dict(arrowstyle="->",
                                           connectionstyle="arc3"))

        else:
            x,y = X[route[i]],  Y[route[i]]
            x1,y1= X[route[i+1]], Y[route[i+1]]
            ax[1].annotate("",
                           xy=(x, y), xycoords='data',
                           xytext=(x1,y1), textcoords='data',
                           arrowprops=dict(arrowstyle="->",
                                           connectionstyle="arc3"))

    textstr = "N Cities: %d\n Total length KM: %.3f" % (N, distance)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(-0.1, -0.1, textstr, transform=ax[1].transAxes, fontsize=14,  # Textbox
               verticalalignment='top', bbox=props)
    plt.title(f"{algorithm_name}-{N}")
    plt.tight_layout()
    plt.savefig(
        f'/home/karmel/PycharmProjects/TSP_Hill_and_Simulated_algorithms/results/pathRoute_{algorithm_name}-{N}.png')

def convergance_plot(solutions_fitness_cities,name_algorithm):
    fig1, ax1 = plt.subplots()
    plt.title(f"TSP {name_algorithm} Convergence Graph")
    plt.xlabel("Generation/Iteration")
    plt.ylabel("Fitness Value")

    for key,value in solutions_fitness_cities.items():
        x = [value[0] for value in value[2]]
        y = [value[1] for value in value[2]]
        # plot
        plt.plot(x, y, label=f'{key}-Cities',linestyle="-.")
        # beautify the x-labels
        plt.legend()

    fig1.savefig(
        f"/home/karmel/PycharmProjects/TSP_Hill_and_Simulated_algorithms/results/{name_algorithm}-Convergence.png")


