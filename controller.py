import threading
import paho.mqtt.client as mqtt
import model

threadStarted = False


def startThreads():
    print("Start threads attempt")
    global threadStarted
    if threadStarted:
        return "Threads have started already"
    else:
        threadStarted = True
        # Mqtt
        x = threading.Thread(target=startSubscription)
        x.start()

        return "Starting threads"


# Mqtt thread
def startSubscription():
    print("Mqtt subscription started....")
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("broker.mqttdashboard.com")
    client.subscribe("ii23/telemetry/#")  # subscribe all nodes

    rc = 0
    while rc == 0:
        rc = client.loop()


# Mqtt on message
def on_message(client, userdata, msg):
    print("Got some Mqtt message ")
    print(msg.topic + " " + str(msg.payload))
    model.update_model(msg)
