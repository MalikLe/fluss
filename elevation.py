import urllib.request
import json


def resquest_elevation(lat, lng):
    apikey = "AIzaSyBH2YY_t66XDHsx6GtLEteWw_vqzSJMjt4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = urllib.request.urlopen(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    results = json.load(request).get('results')
    return results[0].get('elevation')
