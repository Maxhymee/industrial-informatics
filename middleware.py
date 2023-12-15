
import requests
import json
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from flask import Flask


robot_data_url = "http://example.com/robot_data"
r = requests.get(robot_data)

if r.status_code == 200:
    # data interpreting as json
    robot_data = r.json()
    # topic name
    mqtt_topic =  ii23/telemetry
    # data publishing as mqtt
    publish.single(mqtt_topic, json.dumps(robot_data), hostname = "broker.mqttdashboard.com")
else:
    print(f"Error when fetching the robot data. Status code: {r.status_code}")