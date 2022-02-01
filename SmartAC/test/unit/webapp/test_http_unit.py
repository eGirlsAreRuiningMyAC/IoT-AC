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



# ----------------------------- TEST AC TEMPERATURE --------------------------------

def test_set_ac_mode_success(client):
    payload = {'value' : "AUTO"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

def test_set_ac_mode_none(client):
    payload = {"value" : 0}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Mode is required."

def test_set_ac_mode_wrong_value(client):
    payload = {"value" : "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO."

def test_set_ac_mode_cool(client):
    payload = {'value' : "COOL"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

def test_set_ac_mode_dry(client):
    payload = {'value' : "DRY"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

def test_set_ac_mode_fan(client):
    payload = {'value' : "FAN"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

def test_set_ac_mode_heat(client):
    payload = {'value' : "HEAT"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

def test_set_ac_mode_eco(client):
    payload = {'value' : "ECO"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/mode', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Mode succesfully recorded"

#---------------- TEST POWER ---------------------------------------------

def test_set_ac_power_invalid(client):
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    current= response_body["value"]
    payload = {'value' : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    if (current=="STOP"):
        assert res["status"] == "Power value is required."
    else:
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"

def test_set_ac_power_wrong_value(client):
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    payload = {'value' : "no"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    if (current == "STOP"):
        assert res["status"] == "Power must be ON or OFF."
    else:
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"

def test_set_ac_power_on(client):
    res = client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    #assert res.status_code == 200
    current=response_body["value"]
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    cleaning = response_body["value"]
    payload = {'value' : "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob,follow_redirects=True)
    res = json.loads(rv.data.decode())
    if (cleaning=="START"):
        assert rv.status_code == 400
        assert res["status"] == "The device is currently being cleaned and cannot be turned on or off"
    else:
        assert rv.status_code == 200
        if (current=="ON"):
            assert res["status"] == "The air conditioning is already turned on"
        else:
            assert res["status"] == "The air conditioning has been turned on."

def test_set_ac_power_off(client):
    res = client.get("/settings/power")
    response_body = json.loads(res.data.decode())
    # assert res.status_code == 200
    current = response_body["value"]
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    cleaning = response_body["value"]
    payload = {'value' : "OFF"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/power', data=json_ob,follow_redirects=True)
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

#---------------- TEST FANSPEED ---------------------------------------------

def test_set_ac_fan_speed_low(client):
    payload = {'value': "LOW"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

def test_set_ac_fan_speed_medium(client):
    payload = {'value': "MEDIUM"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

def test_set_ac_fan_speed_high(client):
    payload = {'value': "HIGH"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fan speed succesfully recorded"

def test_set_ac_fan_speed_wrong_value(client):
    payload = {"value" : "ON"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Fan speed must be LOW, MEDIUM or HIGH."

def test_set_ac_fan_speed_invalid(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/fanSpeed', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Fan speed is required."

#---------------- TEST HEALTHSCORE ---------------------------------------------

def test_set_ac_health_score_invalid(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/health', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Health score is required."

def test_set_ac_health_score_too_low(client):
    payload = {"value" : -1}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/health', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Health score must be integer between 1 and 10."

def test_set_ac_health_score_too_high(client):
    payload = {"value" : 15}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/health', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Health score must be integer between 1 and 10."

def test_set_ac_health_score_success(client):
    payload = {"value" : 5}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/health', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Health score succesfully recorded"

#---------------- TEST LIGHT ---------------------------------------------

def test_set_ac_light_invalid(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Light value is required."

def test_set_ac_light_wrong_value(client):
    payload = {"value" : "open"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Light must be ON or OFF."

def test_set_ac_light_without_intensity(client):
    payload = {"value" : "ON", "intensity": 0}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Intensity is required if you want to turn the light on."

def test_set_ac_light_with_low_intensity(client):
    payload = {"value" : "ON", "intensity": -10}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Light intensity must be integer between 1 and 100."

def test_set_ac_light_with_high_intensity(client):
    payload = {"value" : "ON", "intensity": 1000}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Light intensity must be integer between 1 and 100."

def test_set_ac_light_with_intensity_success(client):
    payload = {"value" : "ON", "intensity": 60}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Light is now on with intensity 60"

def test_set_ac_light_off(client):
    payload = {"value" : "OFF"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/light', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Light is now off"

#---------------- TEST SOUND ---------------------------------------------

def test_set_ac_sound_invalid(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Sound value is required."

def test_set_ac_sound_wrong_value(client):
    payload = {"value" : "Yes"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Sound must be ON or OFF."

def test_set_ac_sound_on_with_no_volume(client):
    payload = {"value" : "ON", "volume" : 0}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Volume is required if you want to turn the sound on."

def test_set_ac_sound_with_low_volume(client):
    payload = {"value" : "ON", "volume" : -50}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Sound volume must be integer between 1 and 100."

def test_set_ac_sound_with_high_volume(client):
    payload = {"value" : "ON", "volume" : 150}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Sound volume must be integer between 1 and 100."

def test_set_ac_sound_on_success(client):
    payload = {"value" : "ON", "volume" : 70}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Sound is now on with volume 70"

def test_set_ac_sound_off_success(client):
    res = client.get("/settings/sound")
    response_body = json.loads(res.data.decode())
    val= response_body["value"]
    payload = {"value" : "OFF"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/sound', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    if (val=="OFF"):
        assert res["status"] == "The sound is already turned off."
    else:
        assert res["status"] == "Sound is now off"

#---------------- TEST CLEANING ---------------------------------------------

def test_set_ac_cleaning_wrong_value(client):
    payload = {"cleaning" : "Yes"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/cleaning', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Cleaning value must be START or STOP."

def test_set_ac_cleaning_invalid(client):
    payload = {"cleaning" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/cleaning', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Cleaning value is required."

def test_set_ac_cleaning_start(client):
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    current= response_body["value"]
    payload = {"cleaning" : "START"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/cleaning', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    if (current=="START"):
        assert res["status"] == "The device is currently being cleaned."
    else:
        assert res["status"] == "Cleaning value succesfully recorded"

def test_set_ac_cleaning_stop(client):
    res = client.get("/settings/cleaning")
    response_body = json.loads(res.data.decode())
    current = response_body["value"]
    payload = {"cleaning" : "STOP"}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/cleaning', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    if (current=="STOP"):
        assert res["status"] == "The device is currently not being cleaned."
    else:
        assert res["status"] == "Cleaning value succesfully recorded"

def test_set_temperature_too_low(client):
    payload = {"value" : 3}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Temperature must be between 16 and 28"

def test_set_temperature_too_high(client):
    payload = {"value" : 30}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Temperature must be between 16 and 28"

def test_set_temperature_success(client):
    payload = {"value" : 20}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Temperature succesfully recorded"

def test_set_temperature_null_input(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/settings/temperature', data=json_ob)
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
    payload = {"value" : 3}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Air temperature succesfully recorded"

def test_set_air_temperature_null_input(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/temperature', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 400
    assert res["status"] == "Air temperature is required."

def test_set_air_humidity_success(client):
    payload = {"value" : 3}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/humidity', data=json_ob)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Air humidity succesfully recorded"

def test_set_air_humidity_null_input(client):
    payload = {"value" : None}
    json_ob = json.dumps(payload)
    print(json_ob)
    rv = client.post('/air/humidity', data=json_ob)
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

#---------------- TEST PREFERENCE ---------------------------------------------

def test_add_preference_valid(client):
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

def test_add_preference_without_temperature(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": None, "mode": None, "fanSpeed": None, "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Temperature value is required."

def test_add_preference_without_mode(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": None, "fanSpeed": None, "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Mode is required."

def test_add_preference_without_fanspeed_wrong_mode(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "OFF", "fanSpeed": None, "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] == "Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO."

def test_add_preference_without_fanspeed_right_mode(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": None, "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Fan speed is required."

def test_add_preference_without_light_wrong_fanspeed(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "ON", "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = client.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Fan speed must be LOW, MEDIUM or HIGH."

def test_add_preference_without_light_right_fanspeed(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "LOW", "light":None, "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Light value is required."

def test_add_preference_without_sound_wrong_light(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "LOW", "light":"LOW", "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Light must be ON or OFF."

def test_add_preference_without_sound_right_light(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "LOW", "light":"ON", "sound":None}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Sound value is required."

def test_add_preference_wrong_sound(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"temperature": 20, "mode": "DRY", "fanSpeed": "LOW", "light":"ON", "sound":"LOW"}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/preference', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 400
        assert res["status"] =="Sound must be ON or OFF."

def test_get_preference(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True


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
        payload = {"id": 100}
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
        payload = {"turnOnTime": "10","turnOffTime": "11","preferenceId" : 100}
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


def test_add_schedule_user_success(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": "10", "turnOffTime": "12", "preferenceId": 2}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "Schedule addded."

def test_add_schedule_user_success(client) :
    with client as c:
        with c.session_transaction() as sess:
            sess['user_id'] = '1'
            sess['_fresh'] = True
        payload = {"turnOnTime": "10", "turnOffTime": "12", "preferenceId": 2}
        json_ob = json.dumps(payload)
        print(json_ob)
        rv = c.post('/schedule', data=json_ob)
        res = json.loads(rv.data.decode())
        assert rv.status_code == 200
        assert res["status"] == "Schedule addded."




