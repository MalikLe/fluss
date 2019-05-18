import pandas as pd


def read_map(i, ad):
    """Read the maps (layers) from CSV

    Attributes:
        i (string): id of the location
        ad (string): addresse of the location
    """

    # Declaration
    global address
    global id
    global elevation
    global sea_level
    global coord

    # Set global variables
    address = ad
    id = i
    coord_name = 'data/coord_' + str(id) + '.csv'
    data_name = 'data/map_' + str(id) + '.csv'

    # Read layers file
    elevation = pd.read_csv(data_name, header=None, sep=',')
    coord = pd.read_csv(coord_name, header=None, sep=',')

    # Initialize sea level
    sea_level = 0
