import requests
from datetime import datetime, timedelta
import json

api_key = "d69d339320772a7d700ab9f724a86d3e"
base_url = "http://api.openweathermap.org/data/2.5/weather"

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

    current_date = start_date

    weather_data = {}

    while current_date < end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        weather_data[date_str] = get_weather(location)
        current_date += timedelta(days=1)
    
    # Save the weather data to a file
    with open(f"{year}_{month}_weather_data.json", 'w') as file:
        json.dump(weather_data, file)

