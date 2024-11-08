from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from plotly import utils
import json

app = Flask(__name__)
app.debug = True

def generate_figure(request):
    selected_option = request.form.get('SelectVis')

    if selected_option == 'linear':
        data = {
            'Name': ['A', 'B', 'C', 'D'],
            'Value': [10, 15, 7, 12]
    }
    elif selected_option == 'random':
        data = {
            'Name': ['E', 'F', 'G', 'H'],
            'Value': [100, 15, 7, 12]
    }
    else:
        return "Error occured in form submission"

    df = pd.DataFrame(data)

    # Create a Plotly figure
    fig = px.bar(df, x='Name', y='Value', title=df.iloc[0]['Name'])

    # Convert the figure to JSON format
    graphJSON = json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/", methods = ['GET', 'POST'])
def index():
    parameter = None

    if request.method == 'POST':
        parameter = generate_figure(request)

    return render_template('index.html', params = parameter)
