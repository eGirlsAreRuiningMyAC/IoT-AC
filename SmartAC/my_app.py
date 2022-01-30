from flask import Flask, jsonify
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import json
import time

import database
import auth
import environment_api
import environment
import status_api
import status
import settings
import settings_api
import preference_api
import schedule_api
import statistics_api
import ac_statistics

from weather_api_publisher import run_weather_mqtt_client

eventlet.monkey_patch()

app = None
mqtt = Mqtt()
socketio = None
publishThread = None
weatherApiThread = None


def create_app():
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    database.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(environment_api.bp)
    app.register_blueprint(settings_api.bp)
    app.register_blueprint(preference_api.bp)
    app.register_blueprint(schedule_api.bp)
    app.register_blueprint(status_api.bp)
    app.register_blueprint(statistics_api.bp)
    return app


def create_mqtt_app():
    # Connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  
    app.config['MQTT_BROKER_PORT'] = 1883 
    app.config['MQTT_USERNAME'] = ''  
    app.config['MQTT_PASSWORD'] = ''  
    app.config['MQTT_KEEPALIVE'] = 5  
    app.config['MQTT_TLS_ENABLED'] = False 

    try:
        global mqtt
        mqtt.init_app(app)
        mqtt.subscribe('smartAC/air')
        mqtt.subscribe('smartAC/health')

        global socketio 
        socketio = SocketIO(app, async_mode="eventlet")
    except:
        return jsonify({'status': 'Broker is not active'}), 403

    create_mqtt_threads()

    return mqtt


def create_mqtt_threads():
    global publishThread
    if publishThread is None:
        publishThread = Thread(target = mqtt_publish_status_thread)
        publishThread.daemon = True
        publishThread.start()

    global weatherApiThread
    if weatherApiThread is None:
        weatherApiThread = Thread(target = run_weather_mqtt_client)
        weatherApiThread.daemon = True
        weatherApiThread.start()

    return 'MQTT threads created'


def mqtt_publish_status_thread():
    while True:
        time.sleep(30)
        with app.app_context():
            statusMessage = json.dumps(status.get_status(), default=str)
            statisticsMessage = json.dumps(ac_statistics.get_all_statistics(), default=str)

        mqtt.publish('smartAC/status', statusMessage)
        mqtt.publish('smartAC/statistics', statisticsMessage)
    
    

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    data = message.payload.decode("utf-8")
    print('Received message on topic {}: {}'.format(topic, data))

    data = json.loads(data)
    with app.app_context():
        if topic == "smartAC/air":
            airTemperature = data["temp"]
            environment.set_air_temperature(airTemperature)
            environment.update_temperature_auto(airTemperature)
            environment.set_air_humidity(data["humidity"])
        if topic == "smartAC/light":
            settings.set_ac_light_auto(data["intensity"])
        if topic == "smartAC/sound":
            settings.set_ac_sound_auto(data["volume"])
        if topic == "smartAC/health":
            settings.set_ac_health_score(data["health"])


def run_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_app()
    