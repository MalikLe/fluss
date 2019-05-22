import pandas as pd
import matplotlib.pyplot as plt
import scipy.ndimage
import matplotlib.image as mpimg
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import maps
import plot


def update(val):
    """Update water level on the 2D map when the slider move.

    Attributes:
        val (float): value of the water level from the slider

    Todo:
        * Express the sea level relatively to the elevation.
    """
    maps.sea_level = val
    # Redraw the 2D map
    generate_elevation_map(maps.address, maps.id, maps.sea_level, plot.show_img)
    plt.draw()


def generate_flood_map(altitudes, sea_level):
    """Generate the layer of flooded area.

    Attributes:
        altitudes (:array:float): array of altitudes.
        sea_level (float): level of the water.

    Return:
        data (:array:int): array of flooded area.
        proportion_flooded (float): proportion of tiles flooded.
    Todo:
        * Optimize the model (add rules of flooding)
    """
    # Initialize the flood map
    row = range(len(altitudes))
    col = range(len(altitudes))
    n_cases = pow(len(altitudes), 2)
    # Initialize flooded tile counter
    count = 0
    data = pd.DataFrame(data=0, columns=col, index=row)
    # For each tile compare if it is below the sea level
    for i in range(len(altitudes)):
        for j in range(len(altitudes[i])):
            if altitudes[i][j] <= sea_level:
                data[i][j] = 1
                count += 1
    # Compute the proportion of tile flooded
    proportion_flooded = count / n_cases
    return data, proportion_flooded


def generate_elevation_map(address, id, sea_level, show_img):
    """Generate the layer of altitudes and show it.

    Attributes:
        address (string): address of the location
        id (int): id of the location
        sea_level (float): level of the water.
        show_img (bool): if True then show the satellite picture
    """
    # Spline interpolation of the altitudes map
    altitudes = scipy.ndimage.zoom(maps.elevation, 3)
    flood, prop_flood = generate_flood_map(altitudes, sea_level)
    # Initialize rows and columns
    X = [[i for i in range(len(altitudes))] for j in range(len(altitudes))]
    Y = [[j for i in range(len(altitudes))] for j in range(len(altitudes))]
    X = pd.DataFrame(data=X)
    Y = pd.DataFrame(data=Y)

    # Clean the plot
    plot.ax.cla()

    # Plot the flooded layer
    CS_flood = plot.ax.contourf(
                            Y, X, flood, 1, colors='none',
                            hatches=['', '/////'])
    states, labels = CS_flood.legend_elements()
    plt.legend(
                states, ['not flooded', 'flooded'],
                handleheight=2, bbox_to_anchor=(1.13, 5))
    # Plot the isohypses (elevation curves) layer
    CS_alti = plot.ax.contour(
        X, Y, altitudes, 10, cmap="viridis", linewidths=1)
    plot.ax.clabel(CS_alti, inline=1, fontsize=6, fmt='%.1f')

    # Plot the satellite map layer if True
    if(show_img):
        img = mpimg.imread('images/map_' + str(maps.id) + '.png')
        plot.ax.imshow(img, extent=[0, 60, 0, 60], origin='lower', alpha=0.5)

    # Set plot set_parameters
    # Title
    plot.ax.set_title(
        '{}, {}\n proportion of land flooded =  {:.2f}'.format(
            address, id, prop_flood))
    # Aspect
    plot.ax.set_aspect('equal')
    # Axes
    plot.ax.set_ylim(plot.ax.get_ylim()[::-1])
    plot.ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plot.ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))


def generate_map_3d(sea_level, size, res):
    """Generate the 3d map.

    Attributes:
        altitudes (:array:float): array of altitudes.
        size (int): size of the map (km)
        res (int): resolution of the map (number of elevation mesure per km)

    Todo:
        * Adjust the scales
    """

    map = maps.elevation
    # Compute the number of tiles
    nb_tiles = int(size) * int(res)
    # Initialize the axes
    X = [[-i for i in range(-(nb_tiles-1), 1)] for j in range(nb_tiles)]
    Y = [[j for i in range(nb_tiles)] for j in range(nb_tiles)]
    X = pd.DataFrame(data=X)
    Y = pd.DataFrame(data=Y)
    # Generate the flooded tiles layer
    level, _ = generate_flood_map(map, sea_level)
    # Replace 0s by nan so it doesn't show on the plot
    level.replace(0, np.nan, inplace=True)
    # Shift the sea level at the right elevation
    level = level * sea_level

    # Plot
    ax = plt.axes(projection='3d')
    # Plot the sea level
    ax.plot_wireframe(X, Y, level, color="magenta", alpha=1, linewidths=1)
    # TODO: Adjuste the scale
    # Plot the surface of the terrain
    ax.plot_surface(
                    X, Y, map, cmap="viridis", rstride=1, cstride=1,
                    alpha=0.50, antialiased=True)
    # Plot the isohypses layer
    ax.contour(
                X, Y, map, 10, colors="k",
                linestyles="solid", linewidths=1)
    # Set plot parameters
    # Format the axes
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    # Title
    ax.set_title(
        '{}, {}\n'.format(
            maps.address, maps.id))
    # Rotation animation
    for angle in range(0, 90):
        ax.view_init(30, angle + 180)
        plt.draw()
        plt.pause(.001)
