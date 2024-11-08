from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

@app.route("/", methods = ['GET', 'POST'])
def hello():
    parameter = ""
    if request.method == 'POST':
        parameter = request.form.get('SelectVis')
        print(request.form.get('SelectVis'))
    return render_template('index.html', params = parameter)


'''
data = generate_report()
return render_template("report.html", chart_data=data)

'''