import json
import urllib.request
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import seaborn as sns

def elevation(lat, lng):
    apikey = "AIzaSyBH2YY_t66XDHsx6GtLEteWw_vqzSJMjt4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = urllib.request.urlopen(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    results = json.load(request).get('results')
    print(results[0].get('elevation'))


geolocator = Nominatim(user_agent="malik.lechekhab@unil.ch")
km = .015060
resolution = 5
location = geolocator.geocode("les verrières suisse")
lat = location.latitude
lng = location.longitude
originLat = lat - (resolution / 2) * km
originLng = lng - (resolution / 2) * km
areaSize = 5 * 0.015060
alt = map

lats = [originLat + i * km for i in range(resolution)]
lngs = [originLng + i * km for i in range(resolution)]

map = pd.DataFrame(data=None, index=lats, columns=lngs)

print(map)
for i in range(len(lats)):
    for j in range(len(lngs)):
        map.iloc[i, j] = random.random()



# elevation(lat, lng)
