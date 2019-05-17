import requests

api_key = "AIzaSyDfplxEDp5BdGp_2n3Z68pLLwWcMY9CXgU"

# url variable store url
# url = "https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318&markers=color:red%7Clabel:C%7C40.718217,-73.998284&key=AIzaSyDfplxEDp5BdGp_2n3Z68pLLwWcMY9CXgU"

zl = "14"
center = "46.08065218, 7.40284907"
url = "https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center=46.08065218, 7.40284907&zoom="+zl+"&format=png&maptype=satellite&style=feature:administrative%7Celement:geometry%7Cvisibility:off&style=feature:administrative.land_parcel%7Celement:labels%7Cvisibility:off&style=feature:poi%7Cvisibility:off&style=feature:poi%7Celement:labels.text%7Cvisibility:off&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:road.local%7Celement:labels%7Cvisibility:off&style=feature:transit%7Cvisibility:off&size=600x600"


# center defines the center of the map,
# equidistant from all edges of the map.


# zoom defines the zoom
# level of the map

# get method of requests module
# return response object
r = requests.get(url)

# wb mode is stand for write binary mode
f = open('map1.png ', 'wb')

# r.content gives content,
# in this case gives image
f.write(r.content)

# close mthod of file object
# save and close the file
f.close()
