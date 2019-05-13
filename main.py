import pandas as pd
from elevation import resquest_elevation
import matplotlib.pyplot as plt
from haversine import haversine
from mpl_toolkits.mplot3d import axes3d
import scipy.ndimage
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.ticker import FormatStrFormatter


def get_unit(latitude, longitude):
    p1_lng = (latitude, longitude)
    p2_lng = (latitude, longitude + 1)
    p1_lat = (latitude, longitude)
    p2_lat = (latitude + 1, longitude)
    dist_lng = haversine(p1_lng, p2_lng)
    dist_lat = haversine(p1_lat, p2_lat)
    delta_lng = 1 / dist_lng
    delta_lat = 1 / dist_lat

    return delta_lat, delta_lng


def download_map(latitude, longitude, size, res):
    center_lng = longitude
    center_lat = latitude
    unit_lat, unit_lng = get_unit(latitude, longitude)
    unit_lng = unit_lng / res
    unit_lat = unit_lat / res
    origin_lng = center_lng - ((size * res / 2) * unit_lng)
    origin_lat = center_lat + ((size * res / 2) * unit_lat)
    col = [i for i in range(size * res)]
    row = [i for i in range(size * res)]
    coord = pd.DataFrame(data=None, columns=col, index=row)
    data = pd.DataFrame(data=None, columns=col, index=row)

    for i in range(size * res):
        lng = origin_lng + i * unit_lng
        for j in range(size * res):
            lat = origin_lat - j * unit_lat
            alt = resquest_elevation(lat, lng)
            coord[i][j] = (lat, lng)
            data[i][j] = alt
    # TODO: Automatized name
    coord.to_csv('coord5.csv', sep=",", index=False, header=False)
    data.to_csv('map5.csv', sep=",", index=False, header=False)
    return data


def flood_map(altitudes, sea_level):
    row = range(len(altitudes))
    col = range(len(altitudes))
    n_cases = pow(len(altitudes), 2)
    count = 0
    data = pd.DataFrame(data=0, columns=col, index=row)
    for i in range(len(altitudes)):
        for j in range(len(altitudes[i])):
            if altitudes[i][j] <= sea_level:
                data[i][j] = 1
                count += 1
    proportion_flooded = count / n_cases
    return data, proportion_flooded


# TODO: Create download manager
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# map = download_map(-54.97736393,-65.46282539, 20, 1)
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------


def generate_map(sea_level):

    altitudes = scipy.ndimage.zoom(map, 3)
    flood, prop_flood = flood_map(altitudes, sea_level)
    # flood = scipy.ndimage.zoom(flood, 3)

    X = [[i for i in range(len(altitudes))] for j in range(len(altitudes))]
    Y = [[j for i in range(len(altitudes))] for j in range(len(altitudes))]

    X = pd.DataFrame(data=X)
    Y = pd.DataFrame(data=Y)

    # ax.contour(Y, X, flood, 0, colors="r")
    ax.cla()

    plt.rcParams['hatch.color'] = 'r'
    plt.rcParams['hatch.linewidth'] = 0.2

    CS_flood = ax.contourf(
                            Y, X, flood, 1, colors='none',
                            hatches=['', '/////'])
    states, labels = CS_flood.legend_elements()
    plt.legend(
                states, ['not flooded', 'flooded'],
                handleheight=2, bbox_to_anchor=(1.13, 5))

    CS_alti = ax.contour(X, Y, altitudes, 10, cmap="viridis", linewidths=1)
    ax.clabel(CS_alti, inline=1, fontsize=6, fmt='%.1f')
    ax.set_title('proportion of land flooded =  {:.2f}'.format(prop_flood))
    ax.set_aspect('equal')
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    # ax.set_xlim(ax.get_xlim()[::-1])


def generate_map_3d(sea_level):
    # X1, Y1, Z = axes3d.get_test_data()
    X = [[-i for i in range(-19, 1)] for j in range(20)]
    Y = [[j for i in range(20)] for j in range(20)]

    X = pd.DataFrame(data=X)
    Y = pd.DataFrame(data=Y)
    level, ratio = flood_map(map, sea_level)
    level.replace(0, np.nan, inplace=True)
    level = level * sea_level

    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, level, color="magenta", alpha=1, linewidths=1)
    ax.plot_surface(
                    X, Y, map, cmap="viridis",
                    lw=3, rstride=1, cstride=1,
                    alpha=0.50, antialiased=True)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.contour(
                X, Y, map, 10, lw=3, colors="k",
                linestyles="solid", linewidths=1)
    for angle in range(0, 90):
        ax.view_init(30, angle + 180)
        plt.draw()
        plt.pause(.001)
    plt.show()


def update(val):
    lvl = slider1.val
    generate_map(lvl)
    plt.draw()


global map
global coord

# TODO: Set file manager
map = pd.read_csv('map.csv', header=None, sep=',')
coord = pd.read_csv('coord.csv', header=None, sep=',')

sea_level = 0

min_alt = map.min().min()
max_alt = map.max().max()
step = int((max_alt - min_alt) / 200)

fig, ax = plt.subplots()

axSlider1 = plt.axes([0.1, 0.05, 0.8, 0.05])
plt.subplots_adjust(left=0.1, bottom=0.15)
slider1 = Slider(
                    axSlider1, 'level:', valmin=min_alt,
                    valmax=max_alt-1, valstep=step)

slider1.on_changed(update)

generate_map(min_alt-10)

plt.show()

generate_map_3d(slider1.val)
