#Imports
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import plotly.express as px
from plotly import utils
import json
import numpy as np
from flask_session import Session
import statistics
from sklearn.linear_model import LinearRegression
# from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA


#App config
app = Flask(__name__)
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SECRET_KEY'] = 'abcd123'
Session(app)

#Routing
@app.route("/", methods = ['GET', 'POST'])
def index():

    if request.method == 'POST':
        parameter, other_info, prediction_param = generate_figure(request)
        session['parameter'], session['other_info'], session['prediction_param'] = parameter, other_info, prediction_param
        return redirect(url_for('index'))

    #use Session to prevent dashboard from appearing upon refresh - assisted by Perplexity AI
    parameter, other_info, prediction_param = session.get('parameter'), session.get('other_info'), session.get('prediction_param')
    session.pop('parameter', None)
    session.pop('other_info', None)
    session.pop('prediction_param', None)

    return render_template('index.html', dashboard=parameter, other = other_info, prediction = prediction_param)


#Ancillary functions
def generate_figure(request):
    selected_option = request.form.get('SelectVis')
    other = None
    #If Linear graph is selected
    if selected_option == 'linear':
        #Fetch Generated Data
        slope = float(request.form.get('slope'))
        intercept = float(request.form.get('intercept'))
        data, other = generate_linear_data(slope, intercept)

        # Create a Plotly figure
        fig = px.line(data, x='Time', y='Value', title="Linear Curve Graph", markers = True,  color_discrete_sequence = ['#410292'])

        r = regressCompute(data)
        fig2 = px.line(r, x='Time', y='Value', title="Linear Prediction Curve (Beta)", markers = True, color = 'Type', color_discrete_sequence = ['#410292', '#54ee54', '#bbbbbb', '#999999'])


    # If random graph is selected
    elif selected_option == 'random':
        #Fetch Generated Data 
        minVal = float(request.form.get('min'))
        maxVal = float(request.form.get('max'))
        data, other = generate_random_data(minVal, maxVal)

        # Create a Plotly figure
        fig = px.line(data, x='Time', y='Value', title="Random Curve Graph", markers = True, color_discrete_sequence = ['#a62910'])

        r = regressCompute(data)
        fig2 = px.line(r, x='Time', y='Value', title="Random Prediction Curve (Beta)", markers = True, color = 'Type', color_discrete_sequence = ['#a62910', '#54ee54', '#bbbbbb', '#999999'])

    else:
        return "Error occured in form submission"

    # Convert the figure to JSON format
    graphJSON = json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    graph2JSON = json.dumps(fig2, cls=utils.PlotlyJSONEncoder)

    return graphJSON, other, graph2JSON

def generate_linear_data(slope, intercept):
    #Generate y = mt + c data

    #Generate time series
    time_range = pd.date_range(start='2024-11-10', end='2024-11-10 23:59', freq='10min')

    x_values = np.arange(0, 60*24, 10).tolist()

    linear_values = [slope*x + intercept for x in x_values]

    time_series_data = pd.DataFrame({'Time': time_range, 'Value': linear_values})
    
    # Fetch other info parameters and values
    other_info = find_other_info(linear_values)
    
    return time_series_data, other_info

def generate_random_data(minval, maxval):
    #Generate random data between min-max boundaries

    time_range = pd.date_range(start='2024-11-10', end='2024-11-10 23:59', freq='10min')

    random_values = np.random.uniform(minval, maxval, size=len(time_range))

    time_series_data = pd.DataFrame({'Time': time_range, 'Value': random_values})

    # Pass numpy.ndarray as a list for processing of other info
    other_info = find_other_info(list(random_values))
    
    return time_series_data, other_info

def find_other_info(values):

    # Create  a dictionary for other info, and send calculated values to the route
    other_info = {}

    #Round values to 3 decimal places for presentation
    other_info['Minimum value'], other_info['Maximum Value'] = round(min(values), 3), round(max(values), 3)
    other_info['Median of the data'], other_info['Mean of the data'] = round(statistics.median(values), 3), round(statistics.mean(values), 3)
    
    return other_info

def regressCompute(df):

    # Fit Auto ARIMA model - Assisted by Perplexity AI
    # Fit ARIMA model
    model = ARIMA(df['Value'], order=(3, 0, 3))  
    model_fit = model.fit()

    # Forecast future values
    forecast = model_fit.get_forecast(steps=37)  # Predict next 37 time points i.e. 6 hours

    # Generate Forecast DF
    time_range = pd.date_range(start='2024-11-11', end='2024-11-11 06:00', freq='10min')

    forecast_df = pd.DataFrame({'Time': time_range, 'Predicted Value': forecast.predicted_mean, "Lower Limit": forecast.conf_int()['lower Value'], "Upper Limit": forecast.conf_int()['upper Value']})

    forecast_df = forecast_df.melt(id_vars=['Time'], value_vars=['Predicted Value', 'Lower Limit', 'Upper Limit'], ignore_index=False, var_name="Type", value_name="Value")

    df['Type'] = 'Actual Value'

    forecast_df = pd.concat([df, forecast_df], sort= False)

    return forecast_df

