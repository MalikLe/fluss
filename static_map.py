import requests


def download_map_sat(lat, lng, id):
    """Download a satellite picture usign Google Static Map API.

    Attributes:
        lat (int): Latitude of the center of the map.
        lng (int): Longitude of the center of the map.
        id (int): Id number of the map.

    Todo:
        * Adjust the zoom level accordingly to the size of the map.
    """
    # Variables affectation
    # Key of the API
    api_key = "AIzaSyDfplxEDp5BdGp_2n3Z68pLLwWcMY9CXgU"
    # Zoom level (20: very close, 1: very far)
    zl = "15"
    # Center of the map
    center = str(lat) + ", " + str(lng)
    # Stype of the map (satellite or roadmap)
    maptype = "satellite"
    # Size of the image
    size = "400x400"
    url = "https://maps.googleapis.com/maps/api/staticmap?key="
    # Build request
    req = (url + api_key + "&center=" + center + "&zoom=" + zl +
           "&format=png&maptype=" + maptype +
           "&style=feature:administrative%7Celement:geometry%7" +
           "Cvisibility:off&style=feature:administrative.land_parcel%7" +
           "Celement:labels%7Cvisibility:off&style=feature:poi%7" +
           "Cvisibility:off&style=feature:poi%7Celement:labels.text%7" +
           "Cvisibility:off&style=feature:road%7Celement:labels.icon%7" +
           "Cvisibility:off&style=feature:road.local%7Celement:labels%7" +
           "Cvisibility:off&style=feature:transit%7Cvisibility:off&size=" +
           size)
    # Set the name of the picture
    name = "images/map_" + str(id) + ".png"
    # Download the picture
    r = requests.get(req)
    # Save the picture
    f = open(name, 'wb')
    f.write(r.content)
    f.close()
