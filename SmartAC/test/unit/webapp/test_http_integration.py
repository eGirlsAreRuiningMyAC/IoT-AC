import pytest
import json
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# going up on the parent directory to reach the directory in which my_app.py is located
parentdir = os.path.dirname(currentdir)
parentdir1 = os.path.dirname(parentdir)
parentdir2 = os.path.dirname((parentdir1))

sys.path.insert(0, parentdir2)

import my_app

@pytest.fixture
def client():

    http_tests_app = my_app.create_app()
    client = http_tests_app.test_client()

    yield client


#----------------------- AUTHENTICATION -------------------------------------

def test_login_and_logout_success(client) :
    data = {"username" : "bianca","password" : "parola"}

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User bianca logged in succesfully"

    rv = client.get('/auth/logout')
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User logged out succesfully"

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User bianca logged in succesfully"

#----------------------------- AC SETTINGS ------------------------------------

def test_multiple_ac_settings(client) :
    # AUTO

    payload = {'value': "AUTO"}
    json_ob = json.dumps(payload)
    rv = client.post('/settings/mode', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

    # FAN

    payload = {'value': "FAN"}
    json_ob = json.dumps(payload)
    rv = client.post('/settings/mode', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

    # HEAT

    payload = {'value': "HEAT"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

    # ECO

    payload = {'value': "ECO"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

    # DRY

    payload = {'value': "DRY"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

    # INVALID VALUE

    payload = {"value": "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO."

    # GET

    res = client.get("/settings/mode")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    assert response_body["status"] == "Mode succesfully retrieved"

# ------------------------ ENVIRONMENT -------------------------------------

def test_multiple_settings_environment(client) :
    #SET

    payload = {"value": 3}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Air temperature succesfully recorded"

    #GET

    res = client.get("/air/temperature")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    if response_body["value"] is not None:
        assert response_body["status"] == "Air temperature succesfully retrieved"
    else:
        assert response_body["status"] == "Please set a value for air temperature first"

    #SET

    payload = {"value": 3}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/humidity', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Air humidity succesfully recorded"

    #GET

    res = client.get("/air/humidity")
    response_body = json.loads(res.data.decode())
    assert res.status_code == 200
    if response_body["value"] is not None:
        assert response_body["status"] == "Air humidity succesfully retrieved"
    else:
        assert response_body["status"] == "Please set a value for air humidity first"

    # INVALID INPUT FOR SET

    payload = {"value": None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Air temperature is required."

    payload = {"value": None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/humidity', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Air humidity is required."

def test_set_auth_and_statistics(client) :
    data = {"username": "bianca", "password": "parola"}

    rv = client.post('/auth/login', data=json.dumps(data))
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User bianca logged in succesfully"

    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        res = c.get("/statistics")
        assert res.status_code == 200

    rv = client.get('/auth/logout')
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "User logged out succesfully"

def test_add_preference_and_schedule(client) :
    # ADD
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "LOW", "light":"ON", "sound":"ON"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] =="Preference addded."

    #GET
        res = c.get("/preference")
        response_body = json.loads(res.data.decode())
        assert res.status_code == 200
        assert response_body["status"] == "These are all your preferences"

    #ADD SCHEDULE
        payload = {"turnOnTime": "10", "turnOffTime": "12", "preferenceId": 2}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "Schedule addded."

    #GET
        rv = c.get("/schedule")
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "These are all your schedules"

def test_start_while_cleaning(client) :
    payload = {"value": 3}
    json_ob = json.dumps(payload)
    rv = client.post('/settings/health', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Health score succesfully recorded"

    payload = {'value': "ON"}
    json_ob = json.dumps(payload)
    rv = client.post('/settings/power', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"

    payload = {"cleaning": "STOP"}
    json_ob = json.dumps(payload)
    rv = client.post('/settings/cleaning', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Cleaning value succesfully recorded"
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    print(current)

    res = client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    cleaning = response_body["value"]
    payload = {'value': "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    if (cleaning == "START"):
        assert rv.status_code == 400
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"
    else:
        assert rv.status_code == 200
        if (current == "ON"):
            assert res["status"] == "The air conditioning is already turned on"
        else:
            assert res["status"] == "The air conditioning has been turned on."

def test_power_switch(client) :
    #ON

    res = client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    cleaning = response_body["value"]
    payload = {'value': "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    if (cleaning == "START"):
        assert rv.status_code == 400
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"
    else:
        assert rv.status_code == 200
        if (current == "ON"):
            assert res["status"] == "The air conditioning is already turned on"
        else:
            assert res["status"] == "The air conditioning has been turned on."

    # OFF

    res = client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    cleaning = response_body["value"]
    payload = {'value': "OFF"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    if (cleaning == "START"):
        assert rv.status_code == 400
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"
    else:
        assert rv.status_code == 200
        if (current == "OFF"):
            assert res["status"] == "The air conditioning is already turned off"
        else:
            assert res["status"] == "The air conditioning has been turned off."

def test_multiple_settings_fan_spped(client) :
    payload = {'value': "LOW"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

    payload = {'value': "MEDIUM"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

    payload1 = {'value': "HIGH"}
    json_ob = json.dumps(payload1)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

    payload = {"value": "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Fan speed must be LOW, MEDIUM or HIGH."

    payload = {"value": None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Fan speed is required."

