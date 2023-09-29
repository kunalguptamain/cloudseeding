import requests
import pandas
from datetime import datetime, timedelta
import json

api_key = "d69d339320772a7d700ab9f724a86d3e"
base_url = "http://api.openweathermap.org/data/2.5/weather"
URL_HISTORICAL = "https://archive-api.open-meteo.com/v1/archive"
MAX_MIN_VALS = {'temperature_2m' : (-20, 60), 
                'relativehumidity_2m' : (0, 100), 
                'dewpoint_2m' : (-10, 20), 
                'surface_pressure' : (800, 900),
                'cloudcover' : (0,100),
                'cloudcover_low' : (0,100),
                'cloudcover_mid' : (0,100),
                'cloudcover_high' : (0,100),
                'windspeed_10m' : (0, 25),
                'windspeed_100m' : (0, 30),
                'winddirection_100m' : (0, 360),
                'precipitation_sum' : (0, 1500),
                'precipitation_hours' : (0, 24),
                'winddirection_10m_dominant' : (0, 360)}

def get_weather(location):
    """
    :param location: a tuple containing the latitude and longitude.
    :return: a dictionary containing the weather data.
    """
    latitude, longitude = location
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        response.raise_for_status()

def list_average(data):
    return sum(data) / len(data)

def bucket(data, constraints):
    min, max = constraints
    bucket_size = (max - min) / 4
    mark_1 = min + bucket_size
    mark_2 = mark_1 + bucket_size
    mark_3 = mark_2 + bucket_size
    print("min: ", min, " max: ", max, " bucket_size: ", bucket_size, " mark_1: ", mark_1, " mark_2: ", mark_2, " mark_3: ", mark_3)
    buckets = [0, 0, 0, 0]

    for data_point in data:
        if data_point < mark_1:
            buckets[0] += 1
        elif data_point < mark_2:
            buckets[1] += 1
        elif data_point < mark_3:
            buckets[2] += 1
        else:
            buckets[3] += 1
    
    return buckets

def save_monthly_weather(location, year, month):
    """
    location: a tuple containing the latitude and longitude.
    year: a string representing the year, "2023".
    month: a string representing the month, "09".
    """
    start_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    # Calculating the last day of the month
    if month == "12":
        end_date = start_date.replace(year=int(year) + 1, month=1)
    else:
        end_date = start_date.replace(month=int(month) + 1)
    end_date -= timedelta(days=1)

    current_date = start_date

    latitude, longitude = location
    PARAMS = {
                'latitude' : latitude,
                'longitude' : longitude,
                'start_date' : start_date.date(),
                'end_date' : end_date.date(),
                'hourly' : ['temperature_2m', 
                            'relativehumidity_2m', 
                            'dewpoint_2m', 
                            'surface_pressure',
                            'cloudcover',
                            'cloudcover_low',
                            'cloudcover_mid',
                            'cloudcover_high',
                            'windspeed_10m',
                            'windspeed_100m',
                            'winddirection_100m'],
                'daily' : ['precipitation_sum',
                           'precipitation_hours',
                           'winddirection_10m_dominant']
             }

    weather_data = {}

    response = requests.get(url=URL_HISTORICAL, params=PARAMS)
    if response.status_code == 200:
        response.raise_for_status()
    
    data = response.json()
    data_hourly = data['hourly']
    data_processed = {}
    for key in data_hourly:
        if key != 'time':
            data_list = data_hourly[key]
            avg = list_average(data_list)
            bucket_list = bucket(data_list, MAX_MIN_VALS[key])
            data_processed[key] = (avg, bucket_list)

    print(data)

    return data_processed

    return data

    while current_date < end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        #weather_data[date_str] = get_weather(location)
        current_date += timedelta(days=1)
    
    # Save the weather data to a file
    with open(f"{year}_{month}_weather_data.json", 'w') as file:
        json.dump(weather_data, file)


temp = save_monthly_weather((40.722651, -115.587235), "2022", "06")
print(temp)