from paho.mqtt import client as mqtt_client
from pip._vendor import requests
import json
import time

broker = 'localhost'
port = 1883
topic = "smartAC/air"
clientId = 'smartAC-mqtt-weatherApi'

OPENWEATHER_KEY = "97012e2cdb78396cf133bce160eb9f14"
OPENWEATHER_CITY_ID = 683503
url = f"http://api.openweathermap.org/data/2.5/weather?id={OPENWEATHER_CITY_ID}&appid={OPENWEATHER_KEY}&type=accurate&units=metric&lang=ro"


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Weather API connected to MQTT Broker")


def connect_mqtt():
    client = mqtt_client.Client(clientId)            
    client.on_connect = on_connect  
    client.connect(broker, port)               
    return client 


def publish(client):
    while True:
        request = requests.get(url)
        data = request.json()
        message = json.dumps({'temp': data["main"]["temp"], 'humidity': data["main"]["humidity"]})
        client.publish(topic, message)
        time.sleep(61)


def run_weather_mqtt_client():
    print("Run weather API client")
    client = connect_mqtt()
    client.loop_start()
    publish(client)
