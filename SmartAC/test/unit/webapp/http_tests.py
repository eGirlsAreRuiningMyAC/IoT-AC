import pytest
import json
from app import create_app


@pytest.fixture
def client():
    http_tests_app = create_app()
    client = http_tests_app.test_client()
    yield client

