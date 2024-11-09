from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import plotly.express as px
from plotly import utils
import json
import numpy as np
from flask_session import Session



#App config
app = Flask(__name__)
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SECRET_KEY'] = 'abcd123'
Session(app)

#Routing
@app.route("/", methods = ['GET', 'POST'])
def index():
    # parameter = None

    if request.method == 'POST':
        parameter = generate_figure(request)
        session['parameter'] = parameter
        return redirect(url_for('index'))

    #use Session to prevent dashboard from appearing upon refresh - assisted by Perplexity AI
    parameter = session.get('parameter')
    session.pop('parameter', None)
    return render_template('index.html', dashboard=parameter)


#Ancillary functions
def generate_figure(request):
    selected_option = request.form.get('SelectVis')

    #If Linear graph is selected
    if selected_option == 'linear':
        #Fetch Generated Data
        slope = float(request.form.get('slope'))
        intercept = float(request.form.get('intercept'))
        data = generate_linear_data(slope, intercept)

        # Create a Plotly figure
        fig = px.line(data, x='Time', y='Value', title="Linear Curve Graph", markers = True,  color_discrete_sequence = ['#410292'])

    # If random graph is selected
    elif selected_option == 'random':
        #Fetch Generated Data 
        minVal = float(request.form.get('min'))
        maxVal = float(request.form.get('max'))
        data = generate_random_data(minVal, maxVal)

        # Create a Plotly figure
        fig = px.line(data, x='Time', y='Value', title="Random Curve Graph", markers = True, color_discrete_sequence = ['#a62910'])

        # Ensure y-axis starts from 0 wherever appropriate
        if (minVal > 0 and maxVal > 0):
            fig.update_yaxes(range = [0,None])

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
    
    return time_series_data

def generate_random_data(minval, maxval):
    #Generate random data between min-max boundaries

    time_range = pd.date_range(start='2024-11-07', end='2024-11-07 23:59', freq='10min')

    random_values = np.random.uniform(minval, maxval, size=len(time_range))

    time_series_data = pd.DataFrame({'Time': time_range, 'Value': random_values})
    
    return time_series_data

