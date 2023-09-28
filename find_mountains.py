import requests
import json

class Mountain:
    def __init__(self, name, coords, max_elevation):
        self.name = name
        self.coords = coords
        self.max_elevation = max_elevation
    
    def __repr__(self):
        output = self.name + " (" + str(self.coords[0]) + "," + str(self.coords[1]) + ") " + str(self.max_elevation)
        return output

class MountainInfo:
    def __init__(self, lat, long, json_data):
        self.lat = lat
        self.long = long
        self.json_data = json_data
        self.mountain_list = []
        self.highest = None

    def add_entry(self, entry):
        self.mountain_list.append(entry)
        if self.highest is None:
            self.highest = entry
        elif entry.max_elevation > self.highest.max_elevation:
            self.highest = entry

    def __repr__(self):
        output = ""
        for entry in self.mountain_list:
            output += entry.__repr__() + "\n"
        return output

#helper function to find highest elevation within 1km square around coords
def highest_elevation(coords, step, key):
    lat = coords[0]
    long = coords[1]
    coords_list = []
    coords_list_google = []

    for step_lat in range(step * -1, step + 1):
        for step_long in range(step * -1, step + 1):
            coords_list.append({
                            "latitude": lat + (step_lat * 0.001), 
                            "longitude": long + (step_long * 0.001)
                        })
            coords_list_google.append(
                            str(lat + (step_lat * 0.001)) + "," + str(long + (step_long * 0.001))
            )
    
    coords_string_google = '|'.join(str(elem) for elem in coords_list_google)

    URL = "https://api.open-elevation.com/api/v1/lookup"
    URL_GOOGLE = "https://maps.googleapis.com/maps/api/elevation/json"
    HEADERS = {"Accept" : "application/json", "Content-Type" : "application/json"}
    PARAMS = {'locations': coords_list}
    PARAMS_GOOGLE = {'locations': coords_string_google, 'key' : key}

    response = requests.post(url=URL, headers=HEADERS, json=PARAMS)
    #response = requests.post(url=URL_GOOGLE, params=PARAMS_GOOGLE)
    try:
        data = response.json()
    except:
        print("Failed to get response from Elevation API")
        print("response code ", response)
        exit(0)

    point_list = data['results']
    elevation = 0
    for point in point_list:
        if (point['elevation'] > elevation):
            elevation = point['elevation']
    
    return elevation

#finds searches for 20 nearby mountains, returns MountainInfo object
def find_mountains(lat, long, radius, key):
    URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    PARAMS = {'location' : str(lat) + "," + str(long), 'radius' : str(radius), 'keyword' : "mountain|mount|mt", 'type' : 'natural_feature', 'key' : key}
    
    response = requests.get(url=URL, params=PARAMS)
    try:
        data = response.json()
    except:
        print("Failed to get response from Google Place API")
        print("response code ", response)
        exit(0)
    
    places = data['results']
    mountain_info = MountainInfo(lat, long, data)
    basepoint = Mountain("BASEPOINT", (lat, long), highest_elevation((lat,long), 5, key))
    for place in places:
        name = place['name']
        location = place['geometry']['location']
        coords = (location['lat'], location['lng'])
        elevation = highest_elevation(coords, 5, key)
        new_mountain = Mountain(name, coords, elevation)
        mountain_info.add_entry(new_mountain)
    
    return mountain_info

out = find_mountains(44.276884, -71.304156, 25000, "AIzaSyCDZkpWM43ZWy0bJOxOL15JBQRJwBt7tNQ")
print(out)
print(out.highest)