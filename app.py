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
# creating a Flask app
app = Flask(__name__)
CORS(app)

# home page
@app.get('/')
def index_get():
   return render_template('index.html', name=None)

# submit information from home page
@app.post('/submit')
def submit():
   name = request.form.get('name')
   return render_template('index.html', name=name)

@app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.json.get('input_data')
    # Call your Python function with input_data and get the result
    result = KunalsFunction(input_data)
    print(input_data)
    print(result)
    return jsonify(result)



def KunalsFunction(input):
   time.sleep(3)
   return [80.0]
# if you want, you can run this code with the following:
# > 
# driver function: go to http://127.0.0.1:5000 to see
# Port 5000 can be any port
if __name__ == "__main__":
  app.run(debug=True, port=5002)