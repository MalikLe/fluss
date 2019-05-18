from geopy.geocoders import Nominatim
from haversine import haversine


def get_coordinates(address):
    """Geocode an address into coordinates through Nominatim API

    Attributes:
        address (string): address of the location

    Return:
        lat (float): latitude of the address
        lng (float): longitude of the address
    """
    # Set Nominatim session
    geolocator = Nominatim(user_agent="malik.lechekhab@unil.ch")
    # Geocode the address
    location = geolocator.geocode(address)
    # Get coordinates
    lat = location.latitude
    lng = location.longitude

    return lat, lng


def get_unit(latitude, longitude):
    """Compute degrees increment for 1 km at a given latitude using haversine

    Attributes:
        latitude (float): latitude of the address
        longitude (float): longitude of the address

    Return:
        delta_lat (float): degrees per km (latitude)
        delta_lng (float): degrees per km (longitude)
    """
    # Origin point
    p1 = (latitude, longitude)
    # Point one degree farther to the east
    p2_lng = (latitude, longitude + 1)
    # Point one degree farther to the south
    p2_lat = (latitude + 1, longitude)
    # Compute the distance in km
    dist_lng = haversine(p1, p2_lng)
    dist_lat = haversine(p1, p2_lat)
    # Normalize the distance for 1 km
    delta_lng = 1 / dist_lng
    delta_lat = 1 / dist_lat

    return delta_lat, delta_lng
