from paho.mqtt import client as mqtt_client
import json
import time
import random

broker = 'localhost'
port = 1883
clientId = 'smartAC-mqtt-mockData'

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Mock data publisher connected to MQTT Broker")


def connect_mqtt():
    client = mqtt_client.Client(clientId)            
    client.on_connect = on_connect  
    client.connect(broker, port)               
    return client 


def publish(client):
    while True:
        randomValue = random.randint(0,100)
        message = json.dumps({'value': randomValue})
        client.publish("smartAC/env/light", message)

        randomValue = random.randint(0,10)
        message = json.dumps({'value': randomValue})
        client.publish("smartAC/health", message)

        randomValue = random.randint(0,100)
        message = json.dumps({'value': randomValue})
        client.publish("smartAC/env/sound", message)
        time.sleep(10)


def run_mock_data_mqtt_client():
    print("Run mock data client")
    client = connect_mqtt()
    client.loop_start()
    publish(client)
