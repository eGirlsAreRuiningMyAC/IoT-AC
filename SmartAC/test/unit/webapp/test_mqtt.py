import pytest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir1 = os.path.dirname(parentdir)
parentdir2 = os.path.dirname((parentdir1))

sys.path.insert(0, parentdir2)

import my_app

@pytest.fixture
def client():
    my_app.create_app()
    mqtt_app = my_app.create_mqtt_app()

    yield mqtt_app


def on_publish(client, userdata, result):
    print("Data published")
    pass

def test_mqtt_publish(client):
    data = "Test payload for MQTT"
    client.on_publish = on_publish
    result = client.publish("smartAC/status", data, 1)
    assert result[0] == 0

