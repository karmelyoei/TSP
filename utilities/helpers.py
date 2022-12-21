import numpy as np
from matplotlib import pyplot as plt
import geopandas as gpd



def graph_series(list_of_execution_time):
    from matplotlib import pyplot

    values = {}
    for element in list_of_execution_time:
        if element[0] not in values:
            values[element[0]] = [(element[2] - element[1])]
        else:
            values[element[0]].append(element[2] - element[1])
    for key, value in values.items():
        pyplot.plot(value, markersize=20, label=key)
    pyplot.legend()
    pyplot.show()


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
    worldmap.plot(color="lightgrey", ax=ax)

    for Longitude, Latitude in world_cities:
        # Plotting our Impact Energy data with a color map
        x = Longitude
        y = Latitude
        plt.scatter(x, y, s=20, c='blue', alpha=0.6, vmin=0, vmax=20,
                    cmap='autumn')
    # Creating axis limits and title
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])

    plt.title("TSP WorldCities")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()