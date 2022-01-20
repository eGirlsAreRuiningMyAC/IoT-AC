import pytest
from app import create_mqtt_app


@pytest.fixture
def client():
    mqtt_tests_app = create_mqtt_app()
    client = mqtt_tests_app.test_client()
    yield client
