import datetime
import pandas as pd


def add_location(address, lat, lng, size, res):
    """Add a new location to the database CSV

    Attributes:
        address (string): addresse of the location
        lat (float): latitude of the center of the map
        lng (float): longitude of the center of the map
        size (int): size of the map in km
        res (int): resolution of the map (elevation measure per km)

    Return:
        ts (int): time stamp identifier
    """
    # Get the current tim
    d = datetime.datetime.now()
    # Build a timestamp
    ts = (str(d.year) + str(d.month) + str(d.day)
          + str(d.hour) + str(d.minute) + str(d.second))
    # Add the new location to the database
    df2 = pd.DataFrame(
        data=[[ts, address, lat, lng, size, res]], columns=['Id', 'Address', 'Lat', 'Lng', 'Size', 'Res'])
    with open('data/database.csv', 'a') as f:
        df2.to_csv(f, header=False, index=False)
    return ts


def get_info_from_index(index):
    """Get the information of a location given its index

    Attributes:
        index (string): index of the location

    Return:
        id (int): Id of the add_location
        addresse (string): address of the location
        size (int): size of the map
        res (int): resolution of the map
    """
    index = int(index)
    # Read the database of locations
    df = pd.read_csv('data/database.csv', sep=',')
    # Get the variables
    id = df.loc[index, 'Id']
    address = df.loc[index, 'Address']
    size = df.loc[index, 'Size']
    res = df.loc[index, 'Res']
    
    return id, address, size, res


def show_infos():
    """Show the available location in the database
    """
    df = pd.read_csv('data/database.csv', sep=',')
    print(df)
