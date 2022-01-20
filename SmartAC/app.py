from flask import Flask, jsonify
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import json
import time

import database
import auth
import environment
import status_api
import status
import settings
import preference
import schedule
import statistics

eventlet.monkey_patch()

app = None
mqtt = None
socketio = None
thread = None

def create_app():
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    @app.route('/')
    def hello_world():
        global thread
        if thread is None:
            thread = Thread(target=mqtt_thread)
            thread.daemon = True
            thread.start()
        return 'Hello World!'

    database.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(preference.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(status_api.bp)
    app.register_blueprint(statistics.bp)
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
        mqtt = Mqtt(app)
        global socketio 
        socketio = SocketIO(app, async_mode="eventlet")
    except:
        return jsonify({'status': 'Broker is not active'}), 403

    return mqtt


def mqtt_thread():
    while True:
        time.sleep(1)
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
        mqtt.publish('smartAC/mqtt', message)


def run_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_app()
    