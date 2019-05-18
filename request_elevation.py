import pandas as pd
import urllib.request
import json
from geocoder import get_unit


def resquest_elevation(lat, lng):
    """Send single elevation request through Google Elevation API

    Attributes:
        lat (float): latitude of the center of the map.
        lng (float): longitude of the center of the map.

    Return: results[0].get('elevation') (float): elevation for a given location

    Todo:
        * Parallelize the request!
    """
    # Build request
    apikey = "AIzaSyBH2YY_t66XDHsx6GtLEteWw_vqzSJMjt4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    # Send request
    request = urllib.request.urlopen(
        url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    # Read the result
    results = json.load(request).get('results')

    return results[0].get('elevation')


def download_elevations(latitude, longitude, size, res, id):
    """Create elevation map through request loop

    Attributes:
        latitude (float): latitude of the center of the map.
        longitude (float): longitude of the center of the map.
        size (string): size of the map in km
        res (string): resolution of the map (elevation measure per km)

    Todo:
        * Parallelize the request!
    """
    size = int(size)
    res = int(res)
    center_lng = longitude
    center_lat = latitude

    # Get degrees / km for a given latitude
    unit_lat, unit_lng = get_unit(latitude, longitude)
    unit_lng = unit_lng / res
    unit_lat = unit_lat / res

    # Set the top left point of the map
    origin_lng = center_lng - ((size * res / 2) * unit_lng)
    origin_lat = center_lat + ((size * res / 2) * unit_lat)

    # Initialize row and columns
    col = [i for i in range(size * res)]
    row = [i for i in range(size * res)]

    # Initialize coordonate and elevation dataframe
    coord = pd.DataFrame(data=None, columns=col, index=row)
    data = pd.DataFrame(data=None, columns=col, index=row)

    # For each tile, send an elevation request
    for i in range(size * res):
        # Move one unit to the east
        lng = origin_lng + i * unit_lng
        for j in range(size * res):
            # Move one unit to the south
            lat = origin_lat - j * unit_lat
            # Send elevation request
            alt = resquest_elevation(lat, lng)
            # Save the coordonate of the tile
            coord[i][j] = (lat, lng)
            # Save the elevation of the tile
            data[i][j] = alt
    # Create coordonates CSV
    coord_name = 'data/coord_' + str(id) + '.csv'
    coord.to_csv(coord_name, sep=",", index=False, header=False)
    # Create elevations CSV
    data_name = 'data/map_' + str(id) + '.csv'
    data.to_csv(data_name, sep=",", index=False, header=False)
