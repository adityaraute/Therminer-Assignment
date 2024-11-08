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

    #Pass Linear form parameters to a function
    if selected_option == 'linear':
        data = generate_linear_data(request.form.get('slope'), request.form.get('intercept'))

    elif selected_option == 'random':
        data = generate_random_data(request.form.get('min'), request.form.get('max'))

    else:
        return "Error occured in form submission"

    df = data

    # Create a Plotly figure
    fig = px.scatter(df, x='Time', y='Value', title="Graph")

    # Convert the figure to JSON format
    graphJSON = json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    return graphJSON

def generate_linear_data():
    #Generate y = mt + c data
    pass

def generate_random_data(minval, maxval):
    #Generate random data between min-max boundaries

    time_range = pd.date_range(start='2024-11-07', end='2024-11-07 23:59', freq='10min')

    random_values = np.random.randint(minval, maxval, size=len(time_range))
    time_series_data = pd.DataFrame({'Time': time_range, 'Value': random_values})

    print(time_series_data.head())
    
    return time_series_data

