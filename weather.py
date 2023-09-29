import requests
import find_mountains
from datetime import datetime, timedelta
import json

api_key = "d69d339320772a7d700ab9f724a86d3e"
base_url = "http://api.openweathermap.org/data/2.5/weather"
URL_HISTORICAL = "https://archive-api.open-meteo.com/v1/archive"
MAX_MIN_VALS = {'temperature_2m' : (-20, 60), 
                'relativehumidity_2m' : (0, 100), 
                'dewpoint_2m' : (-10, 20), 
                'surface_pressure' : (800, 1100),
                'cloudcover' : (0,100),
                'cloudcover_low' : (0,100),
                'cloudcover_mid' : (0,100),
                'cloudcover_high' : (0,100),
                'windspeed_10m' : (0, 25),
                'windspeed_100m' : (0, 30),
                'winddirection_100m' : (0, 360),
                'precipitation_sum' : (0, 30),
                'precipitation_hours' : (0, 18),
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
    #print("min: ", min, " max: ", max, " bucket_size: ", bucket_size, " mark_1: ", mark_1, " mark_2: ", mark_2, " mark_3: ", mark_3)
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

def monthly_weather(location, year, month):
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
    #print(end_date)
    response = requests.get(url=URL_HISTORICAL, params=PARAMS)
    print("Weather request status code:", response.status_code)
    data = response.json()
    # print(data)
    # print(data['hourly'])
    data_hourly = data['hourly']
    data_daily = data['daily']
    data_processed = {}
    for key in data_hourly:
        if key != 'time':
            data_list = data_hourly[key]
            avg = list_average(data_list)
            bucket_list = bucket(data_list, MAX_MIN_VALS[key])
            data_processed[key] = (avg, bucket_list)
    for key in data_daily:
        if key != 'time':
            data_list = data_daily[key]
            avg = list_average(data_list)
            bucket_list = bucket(data_list, MAX_MIN_VALS[key])
            data_processed[key] = (avg, bucket_list)

    # print(data)
    # print (data_processed)
    return data_processed

    # while current_date < end_date:
    #     date_str = current_date.strftime("%Y-%m-%d")
    #     #weather_data[date_str] = get_weather(location)
    #     current_date += timedelta(days=1)
    
    # # Save the weather data to a file
    # with open(f"{year}_{month}_weather_data.json", 'w') as file:
    #     json.dump(weather_data, file)


def get_weather_for_loc(lat, long):
    key_names = ['temperature_2m', 
                'relativehumidity_2m', 
                'dewpoint_2m', 
                'surface_pressure',
                'cloudcover',
                'cloudcover_low',
                'cloudcover_mid',
                'cloudcover_high',
                'windspeed_10m',
                'windspeed_100m',
                'winddirection_100m',
                'precipitation_sum',
                'precipitation_hours',
                'winddirection_10m_dominant']
    data_dict = {}
    for key in key_names:
        data_dict[key+'_avg'] = []
        data_dict[key+'_25'] = []
        data_dict[key+'_50'] = []
        data_dict[key+'_75'] = []
        data_dict[key+'_100'] = []
    current_year = datetime.now().year
    current_month = datetime.now().month - 2
    month_str = str(current_month + 1)
    month_str = month_str.zfill(2)
    year_str = str(current_year)
    data = monthly_weather((lat, long), year_str, month_str)
    for key in data:
        data_dict[key+'_avg'].append(data[key][0])
        data_dict[key+'_25'].append(data[key][1][0])
        data_dict[key+'_50'].append(data[key][1][1])
        data_dict[key+'_75'].append(data[key][1][2])
        data_dict[key+'_100'].append(data[key][1][3])
    return data_dict



def tenure_weather(name, state, lat, lng, months, validity):
    current_year = datetime.now().year
    key_names = ['temperature_2m', 
                'relativehumidity_2m', 
                'dewpoint_2m', 
                'surface_pressure',
                'cloudcover',
                'cloudcover_low',
                'cloudcover_mid',
                'cloudcover_high',
                'windspeed_10m',
                'windspeed_100m',
                'winddirection_100m',
                'precipitation_sum',
                'precipitation_hours',
                'winddirection_10m_dominant']
    data_dict = {}
    for key in key_names:
        data_dict[key+'_avg'] = []
        data_dict[key+'_25'] = []
        data_dict[key+'_50'] = []
        data_dict[key+'_75'] = []
        data_dict[key+'_100'] = []
    data_dict['name'] = []
    data_dict['state'] = []
    data_dict['validity'] = []

    for month in months:
        for year in (current_year - 10, current_year - 1):
            month_str = str(month + 1)
            month_str = month_str.zfill(2)
            year_str = str(year)
            data = monthly_weather((lat, lng), year_str, month_str)
            for key in data:
                data_dict[key+'_avg'].append(data[key][0])
                data_dict[key+'_25'].append(data[key][1][0])
                data_dict[key+'_50'].append(data[key][1][1])
                data_dict[key+'_75'].append(data[key][1][2])
                data_dict[key+'_100'].append(data[key][1][3])
            data_dict['name'].append(name)
            data_dict['state'].append(state)
            data_dict['validity'].append(validity)

    return data_dict

