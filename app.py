from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from plotly import utils
import json
import numpy as np

#App config
app = Flask(__name__)
app.debug = True

#Routing
@app.route("/", methods = ['GET', 'POST'])
def index():
    parameter = None

    if request.method == 'POST':
        parameter = generate_figure(request)

    return render_template('index.html', params = parameter)


#Ancillary functions
def generate_figure(request):
    selected_option = request.form.get('SelectVis')

    if selected_option == 'linear':
        #Fetch Generated Data
        data = generate_linear_data(float(request.form.get('slope')), float(request.form.get('intercept')))
         # Create a Plotly figure
        fig = px.scatter(data, x='Time', y='Value', title="Linear Graph")


    elif selected_option == 'random':
        #Fetch Generated Data 
        data = generate_random_data(request.form.get('min'), request.form.get('max'))
        # Create a Plotly figure
        fig = px.scatter(data, x='Time', y='Value', title="Random Graph")

    else:
        return "Error occured in form submission"

    # Convert the figure to JSON format
    graphJSON = json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    return graphJSON

def generate_linear_data(slope, intercept):
    #Generate y = mt + c data

    #Generate time series
    time_range = pd.date_range(start='2024-11-07', end='2024-11-07 23:59', freq='10min')

    x_values = np.arange(0, 60*24, 10).tolist()

    linear_values = [slope*x + intercept for x in x_values]

    time_series_data = pd.DataFrame({'Time': time_range, 'Value': linear_values})#, index = time_range)

    print(time_series_data.head())
    
    return time_series_data

def generate_random_data(minval, maxval):
    #Generate random data between min-max boundaries

    time_range = pd.date_range(start='2024-11-07', end='2024-11-07 23:59', freq='10min')

    random_values = np.random.randint(minval, maxval, size=len(time_range))

    time_series_data = pd.DataFrame({'Time': time_range, 'Value': random_values})

    print(time_series_data.head())
    
    return time_series_data

