from flask import Flask, render_template
from flask import request as flask_request
from requests import request
import sqlite3
import controller

DATABASE = ""
MAX_IDLE_TIME = 5
MAX_DOWN_TIME = 3

app = Flask(__name__)

#Serve dynamic pages

@app.route('/')
def static_page():
    def query_for_robot(name):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM robot WHERE deviceId = '{}' ORDER BY time DESC".format(name))
        state = cursor.fetchone()
        if state:
            return state[0]
        else:
            return None
    rob1 = query_for_robot("rob1")
    rob2 = query_for_robot("rob2")
    rob3 = query_for_robot("rob3")
    rob4 = query_for_robot("rob4")
    rob5 = query_for_robot("rob5")
    rob6 = query_for_robot("rob6")
    rob7 = query_for_robot("rob7")
    rob8 = query_for_robot("rob8")
    rob9 = query_for_robot("rob9")
    rob10 = query_for_robot("rob10")
    return render_template('cover_page.html', rob1 = rob1, rob2 = rob2, rob3 = rob3, rob4 = rob4, rob5 = rob5, rob6 = rob6, rob7 = rob7, rob8 = rob8, rob9 = rob9, rob10 = rob10)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    nID = flask_request.args.get('nID')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT state, time FROM robot WHERE deviceId = 'rob{}' ORDER BY time DESC".format(nID))
    data = cursor.fetchall()
    if data!=[]:
        current_state = data[0][0]
    else:
        current_state = None

    #Getting the time spent in every state
    idle_time = 0
    number_of_idle = 0
    processing_time = 0
    number_of_processing = 0
    down_time = 0
    number_of_down = 0
    alarms = []
    while len(data) > 1:
        delta_time = data[1][1] - data[0][1] # time is the second argumment
        if data[0][0] == "READY-IDLE":
            number_of_idle += 1
            idle_time += delta_time
            if delta_time > MAX_IDLE_TIME:
                alarms.append(("IDLE", data[0][1])) #We report when we had a too long time in idle position
        elif data[0][0] == "READY-PROCESSING-ACTIVE":
            number_of_processing += 1
            processing_time += delta_time 
        else:
            number_of_down += 1
            down_time += delta_time
            if delta_time > MAX_IDLE_TIME:
                alarms.append(("DOWN", data[0][1])) #We report when we had a too long time in idle position
        data.pop(0)

    total_time = idle_time + processing_time + down_time
    return render_template('dashboard.html', nID=nID, state = current_state, processing_perc = processing_time/total_time * 100, idle_perc = idle_time/total_time * 100, down_perc = down_time/total_time * 100, alarms = alarms)

@app.route('/alarms-history', methods=['GET'])
def event_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT state, time, deviceId FROM robot ORDER BY deviceId ASC, time DESC")
    data = cursor.fetchall()
    if data!=[]:
        current_state = data[0][0]
    else:
        current_state = None

    alarms = []
    while len(data) > 1:
        if data[0][2]==data[1][2]: #making sure the next message is from the same robot
            delta_time = data[1][1] - data[0][1] # time is the second argumment
            if data[0][0] == "READY-IDLE":
                if delta_time > MAX_IDLE_TIME:
                    alarms.append((data[0][2], "IDLE", data[0][1])) #We report when we had a too long time in idle position
        elif data[0][0] == "DOWN":
            if delta_time > MAX_IDLE_TIME:
                alarms.append((data[0][2], "DOWN", data[0][1])) #We report when we had a too long time in idle position
        data.pop(0)
    return render_template('alarms.html', alarms = alarms)

if __name__ == '__main__':
    controller.startThreads
    app.run(debug=True)
