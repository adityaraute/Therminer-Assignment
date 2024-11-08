from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

def generate_figure(request):
    selected_option = request.form.get('SelectVis')
    if selected_option == 'linear':
        pass
    elif selected_option == 'random':
        pass
    else:
        return "Error occured in form submission"

    return selected_option + request.form.get('min')

@app.route("/", methods = ['GET', 'POST'])

def hello():
    parameter = ""

    if request.method == 'POST':
        parameter = generate_figure(request)

    return render_template('index.html', params = parameter)


'''
data = generate_report()
return render_template("report.html", chart_data=data)
'''