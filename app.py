#!/usr/bin/env python3

"""

  There are a few ways to run this code:
    > make run-local
  this will run the server on your local network. It's equivalent to
    > flask run
  or 
    > python app.py
  
  There is also
    > make run-public
  which will make the server public, coming from your computer. It's equivalent to
    > flask run --host=0.0.0.0

"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import time
import json
from json import JSONEncoder
import tensorflow as tf
import numpy as np
from data_generation import return_weather


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

# creating a Flask app
app = Flask(__name__)
CORS(app)

@app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.json.get('input_data')
    lat = float(input_data[0])
    long = float(input_data[1])
    # Call your Python function with input_data and get the result
    data = getData(lat, long)

    # i = 1
    # for key in data:
    #    print(i, ") " + key + ": ", data[key][0], sep="")
    #    i += 1

    aug = [data[key][0] for key in data]
    aug.pop(0)
    # aug.append(lat)
    # aug.append(long)
    two_dimensional_array = np.array(aug)[np.newaxis,: ]
    # print(aug)

    result = getResult(two_dimensional_array)
    return jsonify([round(result[0][0] * 100, 3), data])

model = tf.keras.models.load_model("./modelsave/")
model.summary()

def getData(lat, long):
  data = return_weather(lat, long)
  return data


def getResult(data):
   result = model.predict(data)
   return result
   
# if you want, you can run this code with the following:
# > 
# driver function: go to http://127.0.0.1:5000 to see
# Port 5000 can be any port
if __name__ == "__main__":
  app.run(debug=True, port=5002)