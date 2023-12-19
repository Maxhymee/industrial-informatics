import json
import sqlite3
from datetime import datetime, timedelta


def archive_message(msg):
    data_str = msg.payload.decode('utf-8')
    data_json = json.loads(data_str)
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("INSERT INTO DeviceStateHistory VALUES (:deviceId,:state, :time)",
              {'deviceId': data_json['deviceId'], 'state': data_json['state'], 'time': data_json['time'][:19]})
    conn.commit()
    conn.close()


# Real-time
def get_latest_state(deviceId):
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("""SELECT state FROM DeviceStateHistory
               WHERE deviceId = :deviceId
               AND time = (SELECT MAX(time) FROM DeviceStateHistory WHERE deviceId = :deviceId)""",
              {'deviceId': deviceId})
    state = c.fetchall()[0][0]
    print(state)
    conn.close()
    return state


# Historical data
def get_states(deviceId, start_time, end_time):
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("""SELECT state, time FROM DeviceStateHistory
               WHERE deviceId = :deviceId
               AND time >= :start_time
               AND time <= :end_time""",
              {'deviceId': deviceId, 'start_time': start_time, 'end_time': end_time})
    rows = c.fetchall()
    conn.close()
    return rows


# Percentage of time in each state
def get_POTIES(deviceId, start_time, end_time):
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("""SELECT state, COUNT(state) FROM DeviceStateHistory
              WHERE deviceId = :deviceId
              AND time >= :start_time
              AND time <= :end_time
              GROUP BY state""",
              {'deviceId': deviceId, 'start_time': start_time, 'end_time': end_time})
    rows = c.fetchall()
    conn.close()
    total = sum(row[1] for row in rows)
    poties = [(row[0], round(100 * row[1] / total)) for row in rows]
    return poties


# Mean Time between Failures
def get_MTBF(deviceId, start_time, end_time):
    rows = get_states(deviceId, start_time, end_time)
    formatted_rows = [(state, datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')) for state, time in rows]
    tbfs = []
    for i in range(1, len(formatted_rows)):
        if formatted_rows[i][0] != 'DOWN' and formatted_rows[i-1][0] == 'DOWN':
            tbf = formatted_rows[i][1] - formatted_rows[i-1][1]
            tbfs.append(tbf)
    if len(tbfs) == 0:
        return 0
    else:
        return sum(tbfs, timedelta())/len(tbfs)


# Alarms

if __name__ == '__main__':
    print(get_POTIES('rob1', '2023-12-15T11:57:03', '2024-12-13T21:04:21'))
    print(get_MTBF('rob1', '2023-12-15T11:57:03', '2024-12-13T21:04:21'))
