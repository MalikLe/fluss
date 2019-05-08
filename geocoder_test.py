import csv
import urllib.request
import json
import numpy as np
import seaborn as sns
import pandas as pd


def elevation(lat, lng):
    apikey = "AIzaSyBH2YY_t66XDHsx6GtLEteWw_vqzSJMjt4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = urllib.request.urlopen(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    results = json.load(request).get('results')
    return results[0].get('elevation')


# TODO: Create dataframe
def get_altitudes_csv():
    # with open('altitudes.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     altitudes = list(reader)
    # while([] in altitudes):
    #     altitudes.remove([])
    data = pd.read_csv('altitudes.csv', sep=',', engine='python')
    return data


def get_altitudes(lats, lngs):
    altitudes = []
    i = 0
    for lat in lats:
        altitudes.append([])
        for lng in lngs:
            altitude = elevation(lat, lng)
            altitudes
            # altitudes[i].append((lat, lng, altitude))
        i += 1

    return altitudes


def save_altitudes(data):
    # with open('altitudes.csv', 'w') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerows(data)
    # csvFile.close()


def show_map(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            print(data[i][j])
        print("\n")


lng = 6.580700
lat = 46.901528
res = 10
unit = 1 / 111
# origin_lng = lng - res / 2 * unit
origin_lat = lat - res / 2 * unit
lats = [origin_lat + i * unit for i in range(res)]
lngs = [lng]

# data = get_altitudes(lats, lngs)
# save_altitudes(data)

data = np.array(get_altitudes_csv())
# altitudes = altitudes.flatten()

print(data[0])
