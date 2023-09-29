import requests
import json

URL_OPEN_ELEVATION = "https://api.open-elevation.com/api/v1/lookup"
URL_GOOGLE_ELEVATION = "https://maps.googleapis.com/maps/api/elevation/json"
URL_GOOGLE_PLACE = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

class Mountain:
    def __init__(self, name, coords, elevation):
        self.name = name
        self.coords = coords
        self.elevation = elevation
    
    def __repr__(self):
        output = self.name + " (" + str(self.coords[0]) + "," + str(self.coords[1]) + ") " + str(self.elevation)
        return output

class MountainInfo:
    def __init__(self, lat, lng, json_data):
        self.lat = lat
        self.lng = lng
        self.json_data = json_data
        self.mountain_list = []
        self.highest = None

    def add_entry(self, entry):
        self.mountain_list.append(entry)
        if self.highest is None:
            self.highest = entry
        elif entry.elevation > self.highest.elevation:
            self.highest = entry

    def __repr__(self):
        output = "Mountains: \n"
        for entry in self.mountain_list:
            output += entry.__repr__() + "\n"
        return output

#helper function to find highest elevation within 1km square around coords
def highest_elevation(coords, step, key):
    lat, lng = coords
    coords_list = []
    coords_list_google = []

    for step_lat in range(step * -1, step + 1):
        for step_long in range(step * -1, step + 1):
            coords_list.append({
                            "latitude": lat + (step_lat * 0.001), 
                            "longitude": lng + (step_long * 0.001)
                        })
            coords_list_google.append(
                            str(lat + (step_lat * 0.001)) + "," + str(lng + (step_long * 0.001))
            )
    
    coords_string_google = '|'.join(str(elem) for elem in coords_list_google)

    HEADERS = {"Accept" : "application/json", "Content-Type" : "application/json"}
    PARAMS = {'locations': coords_list}
    PARAMS_GOOGLE = {'locations': coords_string_google, 'key' : key}

    #response = requests.post(url=URL_OPEN_ELEVATION, headers=HEADERS, json=PARAMS)
    response = requests.post(url=URL_GOOGLE_ELEVATION, params=PARAMS_GOOGLE)

    if response.status_code != 200:
        response.raise_for_status()
        exit(0)
        
    data = response.json()
    point_list = data['results']
    elevation = 0
    for point in point_list:
        if (point['elevation'] > elevation):
            elevation = point['elevation']
    
    return elevation

#finds searches for 20 nearby mountains, returns MountainInfo object
def find_mountains(coords, radius, key):
    lat, lng = coords
    PARAMS = {'location' : str(lat) + "," + str(lng), 'radius' : str(radius), 'keyword' : "mountain|mount|mt", 'type' : 'natural_feature', 'key' : key}
    
    response = requests.get(url=URL_GOOGLE_PLACE, params=PARAMS)

    if response.status_code != 200:
        response.raise_for_status()
        exit(0)
    
    data = response.json()
    places = data['results']
    mountain_info = MountainInfo(lat, lng, data)
    basepoint = Mountain("BASEPOINT", (lat, lng), highest_elevation(coords, 5, key))
    mountain_info.add_entry(basepoint)
    for place in places:
        name = place['name']
        location = place['geometry']['location']
        place_coords = (location['lat'], location['lng'])
        elevation = highest_elevation(place_coords, 5, key)
        new_mountain = Mountain(name, place_coords, elevation)
        mountain_info.add_entry(new_mountain)
    
    return mountain_info

