
from flask import Flask, render_template,request

import threading

import paho.mqtt.client as mqtt


app = Flask(__name__)

threadStarted=False


@app.route('/hello', methods=['GET'])
def helloWorld():
    print("Hello world endpoint")
    return "Hello World"


@app.route('/start', methods=['GET'])
def startThreads():
    print("Start threads attempt")
    global threadStarted
    if (threadStarted):
        return "Threads have started already"
    else:
        threadStarted=True
        #Mqtt
        x = threading.Thread(target=startSubscription)
        x.start()

        return "Starting threads"

#Mqtt on message
def on_message(client, userdata, msg):
    print ("Got some Mqtt message ")
    print(msg.topic+" "+str(msg.payload))

#Mqtt thread
def startSubscription():
    print("Mqtt subscription started....")
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("broker.mqttdashboard.com")
    client.subscribe("ii22/node/#")#subscribe all nodes

    rc = 0
    while rc == 0:
        rc = client.loop()


if __name__ == '__main__':
    app.run()