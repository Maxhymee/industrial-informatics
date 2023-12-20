
import requests
import json
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from flask import Flask

#definitions:
mqtt_topic = "ii23/telemetry"
robot_data_url = "http://broker.mqttdashboard.com:1883/ii23/telemetry"

#function for publishing data from urls (http into mqtt)
def on_message(client, userdata, msg):
    global mqtt_topic
    r = requests.get(msg.payload.decode('utf-8'))
    if r.status_code == 200:
        #data interpreting as json
        robot_data = r.json()
        #topic name
        mqtt_topic =  "ii23/telemetry"
        # data publishing as mqtt
        publish.single(mqtt_topic, json.dumps(robot_data), hostname = "broker.mqttdashboard.com")
    else:
        print(f"Error when fetching the robot data. Status code: {r.status_code}")


subscribe.callback(on_message, topics=[(mqtt_topic, 0)], hostname="broker.mqttdashboard.com")


#right broker? right QoS? Alternative way below?









#alternativ Way:____________________

#import paho.mqtt.subscribe as subscribe
#import paho.mqtt.publish as publish
#import json

#MQTT-Topic
#mqtt_topic = "ii23/telemetry"
#function for publishing
#def on_message(client, userdata, msg):
    #Veröffentliche die empfangenen Daten als MQTT-Nachricht
    #publish.single(mqtt_topic, msg.payload, hostname="broker.mqttdashboard.com")

#subscribe.callback(on_message, topics=[(mqtt_topic, 0)], hostname="hivemq-server.com")
