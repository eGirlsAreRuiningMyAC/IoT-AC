import pytest
import json
from unittest.mock import patch

import sys

sys.path.append("C:/Users/Bianca/Desktop/IS/IoT-AC/SmartAC")

import my_app

@pytest.fixture
def client():

    http_tests_app = my_app.create_app()
    client = http_tests_app.test_client()

    yield client



# ----------------------------- TEST AC TEMPERATURE --------------------------------

def test_set_temperature_too_low(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"value" : 3}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/settings/temperature', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Temperature must be between 16 and 28"

def test_set_temperature_too_high(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
    payload = {"value" : 30}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = c.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Temperature must be between 16 and 28"

def test_set_temperature_success(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
    payload = {"value" : 20}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = c.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Temperature succesfully recorded"

def test_set_temperature_null_input(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = c.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Temperature is required."

def test_get_temperature(client):
    res=client.get("/settings/temperature")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    if response_body["value"] is not None :
        assert response_body["status"] == "Temperature succesfully retrieved"
    else :
        assert response_body["status"] == "Please set a value for temperature"

def test_get_mode(client):
    res=client.get("/settings/mode")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Mode succesfully retrieved"

def test_get_fan_speed(client):
    res=client.get("/settings/fanSpeed")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Fan speed succesfully retrieved"

def test_get_health(client):
    res=client.get("/settings/health")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Health score succesfully retrieved"

def test_get_power(client):
    res=client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "AC power succesfully retrieved"

def test_get_light(client):
    res=client.get("/settings/light")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Light value succesfully retrieved"

def test_get_sound(client):
    res=client.get("/settings/sound")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Sound value succesfully retrieved"

def test_get_cleaning(client):
    res=client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Cleaning value succesfully retrieved"

# ----------------------------- TEST AIR TEMPERATURE --------------------------------

def test_get_air_temperature(client) :
    res = client.get("/air/temperature")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    if response_body["value"] is not None:
        assert response_body["status"] == "Air temperature succesfully retrieved"
    else:
        assert response_body["status"] == "Please set a value for air temperature first"

def test_get_air_humidity(client) :
    res = client.get("/air/humidity")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    if response_body["value"] is not None:
        assert response_body["status"] == "Air humidity succesfully retrieved"
    else:
        assert response_body["status"] == "Please set a value for air humidity first"

def test_set_air_temperature_success(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"value" : 3}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/air/temperature', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "Air temperature succesfully recorded"

def test_set_air_temperature_null_input(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"value" : None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/air/temperature', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Air temperature is required."

def test_set_air_humidity_success(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"value" : 3}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/air/humidity', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "Air humidity succesfully recorded"

def test_set_air_humidity_null_input(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"value" : None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/air/humidity', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Air humidity is required."


# ----------------------------- TEST AC STATISTICS --------------------------------

def test_get_statistics(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        res = c.get("/statistics")
        assert res.status_code == 200

# def test_get_preference(client) :
#     res = client.get("/preference")
#     response_body = json.loads(res.data.decode())
#     assert res.status_code == 200
#     assert response_body["status"] == "These are all your preferences"

#---------------- TEST AUTHENTICATION ---------------------------------------------

def test_register_already_exists_user(client) :
    data = {"username" : "bianca","password" : "parola"}

    rv = client.post('/auth/register', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "User bianca is already registered."

def test_register_null_username(client) :
    data = {"username" : None,"password" : "parola"}

    rv = client.post('/auth/register', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Username is required."

def test_register_null_password(client) :
    data = {"username" : "bia","password" : None}

    rv = client.post('/auth/register', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Password is required."

def test_login_success(client) :
    data = {"username" : "bianca","password" : "parola"}

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User bianca logged in succesfully"

def test_login_invalid_username(client) :
    data = {"username" : "bia","password" : "parola"}

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Username bia not found"

def test_login_invalid_password(client) :
    data = {"username" : "bianca", "password" : "par"}

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Password is incorrect"

def test_logout(client) :
    rv = client.get('/auth/logout')
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User logged out succesfully"

#-------------------------- TEST SCHEDULE ----------------------------

def test_get_schedule(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        rv = c.get("/schedule")
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "These are all your schedules"

def test_delete_schedule_not_found(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"id": 1}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.delete('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "No schedule with this id."

def test_delete_schedule_null_input(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"id": "0"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.delete('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Schedule ID to be deleted is required."


def test_add_schedule_not_found_preference(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": "10","turnOffTime": "11","preferenceId" : 1}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "No preference with this id."

def test_add_schedule_null_turn_on(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": None, "turnOffTime": "11", "preferenceId": "1"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Turn on time is required."

def test_add_schedule_null_turn_off(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": "10", "turnOffTime": None, "preferenceId": "1"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Turn off time is required."

def test_add_schedule_null_preference(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": "10", "turnOffTime": "12", "preferenceId": "0"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Preference ID for this schedule is required."

# def test_delete_schedule_user_not_allowed(client) :
#     TO DO

# def test_delete_schedule_success(client) :
#     TO DO

# def test_add_schedule_user_not_allowed(client) :
#     TO DO

# def test_add_schedule_user_not_success(client) :
#     TO DO