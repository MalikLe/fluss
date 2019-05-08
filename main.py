import pandas as pd
from elevation import resquest_elevation
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


def download_map(latitude, longitude, size, res):
    center_lng = longitude
    center_lat = latitude
    # TODO: Compute the units mathematicaly
    unit_lng = 0.013474 / res
    unit_lat = 0.008972 / res
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
    coord.to_csv('coord.csv', sep=",", index=False, header=False)
    data.to_csv('map.csv', sep=",", index=False, header=False)
    return data


# map = download_map(46.906664, 6.572546, 2, 10)
map = pd.read_csv('map.csv', header=None, sep=',')
coord = pd.read_csv('coord.csv', header=None, sep=',')


sns.kdeplot(map)
sns.heatmap(map, cmap="viridis")
plt.show()

# X1, Y1, Z = axes3d.get_test_data()
X = [[i for i in range(20)] for j in range(20)]
Y = [[j for i in range(20)] for j in range(20)]
X = pd.DataFrame(data=X)
Y = pd.DataFrame(data=Y)
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, map, cmap="viridis", lw=3, rstride=1, cstride=1, alpha=0.5)
ax.contour(X, Y, map, 10, lw=3, colors="k", linestyles="solid", linewidths=1)
plt.show()
