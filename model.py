import json
import sqlite3
from datetime import datetime, timedelta
import time
import threading

monitor_threads = {}
thresholds = {'DOWN': timedelta(minutes=2, seconds=0),
              'READY-IDLE-STARVED': timedelta(minutes=2, seconds=0)}


def update_model(msg):
    # archive the MQTT message into the db
    data_str = msg.payload.decode('utf-8')
    data_json = json.loads(data_str)
    deviceId = data_json['deviceId']
    state = data_json['state']
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("INSERT INTO DeviceStateHistory VALUES (:deviceId,:state, :time)",
              {'deviceId': deviceId, 'state': state, 'time': data_json['time'][:19]})
    conn.commit()
    conn.close()
    # stop and remove the previous monitoring thread if present
    if deviceId in monitor_threads:
        stop_flag = monitor_threads[deviceId][1]
        stop_flag.set()  # Stop the previous monitoring thread
        del monitor_threads[deviceId]
    # create a new monitoring thread with the correct threshold if necessary
    if state in ['DOWN', 'IDLE']:
        monitor_robot_state(deviceId, state)


# Real-time
def get_latest_state(deviceId: str):
    """
    get the latest state and his start time
    for the device link to deviceId

    :return : (state, time)
    """
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("""SELECT state, time FROM DeviceStateHistory
               WHERE deviceId = :deviceId
               ORDER BY time
               DESC LIMIT 1""",
              {'deviceId': deviceId})
    row = c.fetchall()[0]
    conn.close()
    formatted_row = (row[0], datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S'))
    return formatted_row


# Historical data
def get_states(deviceId: str, start_time: str, end_time: str):
    """
    get the states and there start_time
    during the period [start_time, end_time]
    for the device link to deviceId

    :return: [(state, time)]
    """
    conn = sqlite3.connect('Assignment2.db')
    c = conn.cursor()
    c.execute("""SELECT state, time FROM DeviceStateHistory
               WHERE deviceId = :deviceId
               AND time >= :start_time
               AND time <= :end_time""",
              {'deviceId': deviceId, 'start_time': start_time, 'end_time': end_time})
    rows = c.fetchall()
    conn.close()
    formatted_rows = [(state, datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')) for state, time in rows]
    return formatted_rows


# Percentage of time in each state
def get_POTIES(deviceId: str, start_time: str, end_time: str):
    """
    get the percentage of time in each state
    during the period [start_time, end_time]
    for the device link to deviceId

    :return: [pot_idle, pot_processing, pot_down]
    """
    rows = get_states(deviceId, start_time, end_time)
    times = [timedelta(0)] * 3  # [IDLE, PROCESSING, DOWN]
    for i in range(1, len(rows)):
        if rows[i - 1][0] == 'READY-IDLE-STARVED':
            times[0] += rows[i][1] - rows[i - 1][1]
        elif rows[i - 1][0] == 'READY-PROCESSING-EXECUTING':
            times[1] += rows[i][1] - rows[i - 1][1]
        else:
            times[2] += rows[i][1] - rows[i - 1][1]
    total_time = sum(times, timedelta())
    return [round(100 * t / total_time) for t in times]


# Mean Time between Failures
def get_MTBF(deviceId: str, start_time: str, end_time: str):
    """
    get the mean time between failures
    during the period [start_time, end_time]
    for the device link to deviceId

    :return: mtbf
    """
    rows = get_states(deviceId, start_time, end_time)
    tbfs = []
    for i in range(1, len(rows)):
        if rows[i][0] != 'DOWN' and rows[i - 1][0] == 'DOWN':
            tbf = rows[i][1] - rows[i - 1][1]
            tbfs.append(tbf)
    if len(tbfs) == 0:
        return 0
    else:
        return sum(tbfs, timedelta()) / len(tbfs)


# Alarms
def monitor_robot_state(deviceId: str, state: str):
    stop_flag = threading.Event()

    def monitor_state():
        while not stop_flag.is_set():
            latest_state, timestamp = get_latest_state(deviceId)
            if latest_state == state and datetime.now() - timestamp > thresholds[state]:
                print(f"{deviceId} - {state} over threshold")
                stop_flag.set()
            time.sleep(1)
    thread = threading.Thread(target=monitor_state)
    monitor_threads[deviceId] = (thread, stop_flag)
    thread.start()


if __name__ == '__main__':
    print(get_POTIES('rob1', '2023-12-15T11:57:03', '2024-12-13T21:04:21'))
    print(get_MTBF('rob1', '2023-12-15T11:57:03', '2024-12-13T21:04:21'))
