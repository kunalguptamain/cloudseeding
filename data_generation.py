import find_mountains
import weather
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import openpyxl


def store_weather(array):
    key = input("Input Google API Key: ")
    dataframe = pd.DataFrame()
    for entry in array:
        name, state, lat, lng, months, validity = entry
        lng *= -1
        entry_data = weather.tenure_weather(name, state, lat, lng, months, validity)
        mountain_data = find_mountains.find_mountains((lat, lng), 10000, key)
        highest_mountain = mountain_data.highest
        entry_data['highest_elevation'] = [highest_mountain.elevation] * len(entry_data['name'])
        entry_data['highest_elevation_lat'] = [highest_mountain.coords[0]] * len(entry_data['name'])
        entry_data['highest_elevation_lng'] = [highest_mountain.coords[1]] * len(entry_data['name'])
        entry_dataframe = pd.DataFrame(entry_data)
        dataframe = pd.concat([dataframe, entry_dataframe])
    dataframe.to_excel('output.xlsx', index=True)

data = [["Royalston", "MA", 42.6776, 72.1879, [0,1,2,3,4,5,6,7,8,9,10,11], False],
  ["Southbridge", "MA", 42.0751, 72.0334, [0,1,2,3,4,5,6,7,8,9,10,11], False]]
store_weather(data)