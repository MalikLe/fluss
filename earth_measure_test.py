from math import sin, cos, acos, radians, degrees
from haversine import haversine, Unit


def great_circle_distance(lat1, lng1, lat2, lng2):
    lat1_r = radians(lat1)
    lng1_r = radians(lng1)
    lat2_r = radians(lat2)
    lng2_r = radians(lng2)

    a = 6378.1370
    b = 6356.7523

    delta_phi = abs(lat1_r - lat2_r)
    delta_lambda = abs(lng1_r - lng2_r)
    # delta_sigma = acos(sin(lat1_r) * sin(lat2_r) + cos(lat1_r) * cos(lat2_r) * cos(delta_lambda))
    delta_sigma
    d = a * delta_sigma

    print("p = ({}), q = ({})".format((lat1, lng1), (lat2, lng2)))
    print("p = ({}), q = ({})".format((lat1_r, lng1_r), (lat2_r, lng2_r)))
    print("d = ({})".format(d))


def get_boundaries(lat, lng, d):
    a = 6378.1370
    b = 6356.7523

    lat_r = radians(lat)
    lng_r = radians(lng)

    lng2_r = acos((cos(d / a) - sin(lat) * sin(lat)) / (cos(lat) * cos(lat))) + lng_r
    lng2 = degrees(lng2_r)



    print(lng2)


p1 = (46.996792, 6.895455999999999)
p2 = (46.996792, 6.895455999999999 + 1)
print(haversine(p1, p2))
