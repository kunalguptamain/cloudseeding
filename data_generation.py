import find_mountains
import weather
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import openpyxl


def store_weather(array):
    # key = input("Input Google API Key: ")
    key = "AIzaSyCDZkpWM43ZWy0bJOxOL15JBQRJwBt7tNQ"
    dataframe = pd.DataFrame()
    for entry in array:
      name, state, lat, lng, months, validity = entry
      lng *= -1
      entry_data = weather.tenure_weather(name, state, lat, lng, months, validity)
      mountain_data = find_mountains.find_mountains((lat, lng), 10000, key)
      highest_mountain = mountain_data.highest
      entry_data['highest_elevation'] = [highest_mountain.elevation] * len(entry_data['temperature_2m_avg'])
      entry_data['highest_elevation_lat'] = [highest_mountain.coords[0]] * len(entry_data['temperature_2m_avg'])
      entry_data['highest_elevation_lng'] = [highest_mountain.coords[1]] * len(entry_data['temperature_2m_avg'])
      entry_dataframe = pd.DataFrame(entry_data)
      dataframe = pd.concat([dataframe, entry_dataframe], ignore_index=True)
      print("Finished entry")
    dataframe.to_excel('output.xlsx', index=False)

def return_weather(lat, long):
  # key = input("Input Google API Key: ")
  key = "AIzaSyCDZkpWM43ZWy0bJOxOL15JBQRJwBt7tNQ"
  long *= -1
  entry_data = weather.get_weather_for_loc(lat, long)
  mountain_data = find_mountains.find_mountains((lat, long), 10000, key)
  highest_mountain = mountain_data.highest
  entry_data['highest_elevation'] = [highest_mountain.elevation] * len(entry_data['temperature_2m_avg'])
  # entry_data['highest_elevation_lat'] = [highest_mountain.coords[0]] * len(entry_data['temperature_2m_avg'])
  # entry_data['highest_elevation_lng'] = [highest_mountain.coords[1]] * len(entry_data['temperature_2m_avg'])
  
  return entry_data

"""
data = [["Royalston", "MA", 42.6776, 72.1879, [0,1,2,3,4,5,6,7,8,9,10,11], False],
  ["Southbridge", "MA", 42.0751, 72.0334, [0,1,2,3,4,5,6,7,8,9,10,11], False]]
store_weather(data)
"""
# data = [["Elko Mountain", "NV", 40.713775, 115.568607, [0, 1, 2, 3, 4, 10, 11], True],
# ["Riordan", "NV", 40.7266, 115.5859, [0, 1, 2, 3, 4, 10, 11], True],
# ["East Peak", "NV", 8.952500, 119.913038, [0, 1, 2, 3, 4, 10, 11], True],
# ["Granite Peak", "NV", 41.699325, 117.639160, [0, 1, 2, 3, 4, 10, 11], True],
# ["Winnermucca Mountain", "NV", 41.011341, 117.774239, [0, 1, 2, 3, 4, 10, 11], True],
# ["East Manse Rd", "NV", 36.146844, 115.976342, [0, 1, 2, 3, 4, 10, 11], True],
# ["Lee Canyon Ski Area", "NV", 36.3037, 115.6796, [0, 1, 2, 3, 4, 10, 11], True],
# ["Barker Pass", "CA", 39.0763, 120.2338, [0, 1, 2, 3, 4, 10, 11], True],
# ["Bunker Hill", "CA", 38.4265, 120.8291, [0, 1, 2, 3, 4, 10, 11], True],
# ["Northstar Ski Resort", "CA", 39.2647, 120.1332, [0, 1, 2, 3, 4, 10, 11], True],
# ["Spooner Summit", "NV", 39.1043, 119.8972, [0, 1, 2, 3, 4, 10, 11], True],
# ["Sorensen's Resort", "CA", 38.7746, 119.9031, [0, 1, 2, 3, 4, 10, 11], True],
# ["Conway Summit", "CA", 38.0880, 119.1818, [0, 1, 2, 3, 4, 10, 11], True],
# ["Edison Lake", "CA", 37.3818, 118.9732, [0, 1, 2, 3, 4, 10, 11], True],
# ["Mancos", "CO", 37.3450, 108.2892, [0, 1, 2, 3, 4, 10, 11], True],
# ["Purgatory Ski Resort", "CO", 37.6277, 107.8376, [0, 1, 2, 3, 4, 10, 11], True],
# ["Telluride", "CO", 37.9167, 107.8375, [0, 1, 2, 3, 4, 10, 11], True],
# ["western regional climate center", "CO", 41.2123007, 115.4053679, [0, 1, 2, 3, 4, 10, 11], True],
# ["Denver Water", "CO", 39.7350854, 105.0123171, [0, 1, 2, 3, 4, 10, 11], True],
# ["Blue Ridge", "CO", 34.8640, 84.3241, [0, 1, 2, 3, 4, 10, 11], True],
# ["Lake Cachuma", "CA", 34.5790, 119.9480, [0, 1, 2, 3, 4, 10, 11], True],
# ["Gibraltar Dam", "CA", 34.5269, 119.6871, [0, 1, 2, 3, 4, 10, 11], True],
# ["Jameson Reservoir", "CA", 34.4909381, 119.5116917, [0, 1, 2, 3, 4, 10, 11], True],
# ["Twitchell Reservoir", "CA", 34.9988, 120.3327, [0, 1, 2, 3, 4, 10, 11], True],
# ["pleasanton", "TX", 28.9672, 98.4786, [3, 4, 5, 6, 7, 8], True],
# ["San Angelo", "TX", 31.4638, 100.4370, [3, 4, 5, 6, 7, 8], True],
# ["Ogallala Aquifer", "TX", 36.9877, 101.4420, [3, 4, 5, 6, 7, 8], True],
# ["Culberson", "TX", 31.3478, 104.4723, [3, 4, 5, 6, 7, 8], True],
# ["Loving", "TX", 31.8883, 103.6363, [3, 4, 5, 6, 7, 8], True],
# ["Reeves", "TX", 31.4308, 103.7289, [3, 4, 5, 6, 7, 8], True],
# ["Ward", "TX", 28.8439, 96.4641, [3, 4, 5, 6, 7, 8], True],
# ["Red River Valley", "TX", 33.62, 95.05, [3, 4, 5, 6, 7, 8], True],
# ["Logan", "UT", 41.7370, 111.8338, [0, 1, 11], True],
# ["Salt Lake City", "UT", 40.7608, 111.8910, [0, 1, 11], True],
# ["Versnal", "UT", 40.4555, 109.5287, [0, 1, 11], True],
# ["Price", "UT", 39.5994, 110.8107, [0, 1, 11], True],
# ["Richfield", "UT", 38.7725, 112.0841, [0, 1, 11], True],
# ["Saint George", "UT", 37.0965, 113.5684, [0, 1, 11], True],
# ["Colfax", "UT", 39.1007, 120.9533, [3,4,5,6,7,8,9], True],
# ["Curry", "UT", 33.9536, 87.2144, [3,4,5,6,7,8,9], True],
# ["DeBaca", "UT", 34.2734, 104.3792, [3,4,5,6,7,8,9], True],
# ["Eddy", "UT", 47.6964, 98.8872, [3,4,5,6,7,8,9], True],
# ["Guadalupe", "UT", 29.251783, 98.067788, [3,4,5,6,7,8,9], True],
# ["Harding", "UT", 45.5483, 103.5996, [3,4,5,6,7,8,9], True],
# ["Lea", "UT", 51.8919, 2.4961, [3,4,5,6,7,8,9], True],
# ["Lincoln", "UT", 40.5649, 112.2566, [3,4,5,6,7,8,9], True],
# ["Mora", "NM", 35.9730452, 105.4171296, [3,4,5,6,7,8,9], True],
# ["Otero", "UT", 32.6342, 105.5943, [3,4,5,6,7,8,9], True],
# ["Quay", "NM", 35.6526518, 107.1857233, [3,4,5,6,7,8,9], True],
# ["Roosevelt", "UT", 40.2994, 109.9888, [3,4,5,6,7,8,9], True],
# ["San Miguel", "NM", 35.5118, 104.8455 , [3,4,5,6,7,8,9], True],
# ["Union",  "NM", 36.3724, 103.3587, [3,4,5,6,7,8,9], True],
# ["Gordon", "GA", 32.8821, 83.3324, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Shellman", "GA", 31.7563, 84.6152, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Iron City", "GA", 31.0135, 84.8130, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Fargo", "GA", 30.6819, 82.5665, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Alamo", "GA", 32.1471, 82.7779, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Junction City", "GA", 32.6035, 84.4594, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Riddle Ville", "GA", 32.9068, 82.6657, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Florence", "SC", 34.1954, 79.7626, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Lexignton", "SC", 33.9815, 81.2362, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Kitchings Mill", "SC", 33.5785, 81.4773, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Gilbert", "SC", 33.9243, 81.3937, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Bay Springs", "SC", 34.6063, 80.1548, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Abbeville", "SC", 34.1782, 82.3790, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Adamsburg", "SC", 34.7912, 81.5429, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Adams Run", "SC", 32.7207, 80.3482, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Bradley", "SC", 34.0493, 82.2446, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Dorchester", "SC", 33.1680, 80.5438, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Hardeeville", "SC", 32.2871, 81.0807, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Hopkins", "SC", 33.9043, 80.8770, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Martin", "SC", 33.0690, 81.4765, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Altamont", "TN", 35.4295, 85.7230, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Beersheba Springs", "TN", 35.4667, 85.6541, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Cornersville", "TN", 35.3615, 86.8397, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Hendersonville", "TN", 36.3023, 86.6281, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Lakeland", "TN", 35.2306, 89.7404, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Monterey", "TN", 36.1476, 85.2683, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["New Johnsonville", "TN", 36.0265, 87.9839, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Pleasant Hill", "TN", 35.9765, 85.1939, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Sharon", "TN", 36.2334, 88.8245, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Yorkville", "TN", 36.0995, 89.1190, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Adams", "NY", 43.8092, 76.0241, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Bovina", "NY", 42.2695, 74.7268, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Chester", "NY", 41.0018, 73.6657, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Hamden", "NY", 42.1912, 74.9946, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Ithaca", "NY", 42.4440, 76.5019, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Lloyd", "NY", 41.7362, 74.0054, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Lyonsdale", "NY", 43.6187, 75.3063, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Morristown", "NY", 44.5864, 75.6483, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Orleans", "NY", 43.4089, 78.2020, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ['Amherst', "VA", 37.5851, 79.0514, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Capron", "VA", 36.7110, 77.2000, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Lovettsville", "VA", 39.2748, 77.6386, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["New Market", "VA", 38.6479, 78.6714, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Onancock", "VA", 37.7118, 75.7491, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Orange", "VA", 38.2454, 78.1108, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Warrenton", "VA", 38.7135, 77.7953, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Vinton", "VA", 37.2810, 79.8970, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Woodstock", "VA", 38.8818, 78.5058, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Anderson", "NC", 36.2671, 79.3453, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Black", "NC", 35.6179, 82.3212, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Clanton", "NC", 32.8387, 86.6294, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Daviston", "NC", 35.4993, 80.8487, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Auburn", "MA", 42.1945, 71.8356, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Brockton", "MA", 42.0834, 71.0184, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Everett", "MA", 42.4084, 71.0537, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["New Braintree", "MA", 42.3168, 72.1259, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Norwood", "MA", 42.1944, 71.1990, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Royalston", "MA", 42.6776, 72.1879, [0,1,2,3,4,5,6,7,8,9,10,11], False],
# ["Southbridge", "MA", 42.0751, 72.0334, [0,1,2,3,4,5,6,7,8,9,10,11], False]
# ]
# data = [['Amherst', "VA", 37.5851, 79.0514, [0,1,2,3,4,5,6,7,8,9,10,11], False]]
# store_weather(data)

