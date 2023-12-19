from flask import Flask, render_template
from requests import request
import json
import controller

app = Flask(__name__)


#Serve dynamic pages

@app.route('/')
def static_page():
    # Get the last state of all robots
    rob1 = "READY-IDLE-STARVED"
    rob2 = "READY-PROCESSING-EXECUTING"
    return render_template('cover_page.html', rob1 = rob1, rob2 = rob2)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    nID = request.args.get('nID')
    return render_template('dashboard.html')

@app.route('/measurement-history', methods=['GET'])
def measurement_history():
    nID = request.args.get('nID')
    return render_template('measurement.html')

@app.route('/event-history', methods=['GET'])
def event_history():
    nID = request.args.get('nID')
    return render_template('event.html')


if __name__ == '__main__':
    app.run(debug=True)
