from flask import Blueprint, request, jsonify
import settings

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/temperature', methods=['POST'])
def set_ac_temperature_api():
    json = request.get_json(force=True) 
    temperature = json['value']
    if not temperature:
        return jsonify({'status': 'Temperature is required.'}), 400
    if temperature <16 or temperature >28:
        return jsonify({'status': 'Temperature must be between 16 and 28'}), 400
    
    temperatureValue = settings.set_ac_temperature(temperature)
    return jsonify({
        'status': 'Temperature succesfully recorded',
        'value': temperatureValue
         }), 200


@bp.route('/temperature', methods=['GET'])
def get_ac_temperature_api():
    temperature = settings.get_ac_temperature()
    if temperature is None:
        return jsonify({
            'status': 'Please set a value for temperature',
            'value': temperature
        }), 200
    else:
        return jsonify({
            'status': 'Temperature succesfully retrieved',
            'value': temperature
        }), 200


@bp.route('/mode', methods=['POST'])
def set_ac_mode_api():
    json = request.get_json(force=True) 
    mode = json['value']
    if not mode:
        return jsonify({'status': 'Mode is required.'}), 400
    if mode.upper() not in ["AUTO", "COOL", "DRY", "FAN", "HEAT", "ECO"]:
        return jsonify({'status': 'Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO.'}), 400

    modeValue = settings.set_ac_mode(mode.upper())
    return jsonify({
        'status': 'Mode succesfully recorded',
        'value': modeValue
         }), 200



@bp.route('/mode', methods=['GET'])
def get_ac_mode_api():
    mode = settings.get_ac_mode()
    return jsonify({
        'status': 'Mode succesfully retrieved',
        'value': mode
    }), 200


@bp.route('/fanSpeed', methods=['POST'])
def set_ac_fan_speed_api():
    json = request.get_json(force=True) 
    fanSpeed = json['value']
    if not fanSpeed:
        return jsonify({'status': 'Fan speed is required.'}), 400
    if fanSpeed.upper() not in ["LOW", "MEDIUM", "HIGH"]:
        return jsonify({'status': 'Fan speed must be LOW, MEDIUM or HIGH.'}), 400
    
    fanValue = settings.set_ac_fan_speed(fanSpeed.upper())
    return jsonify({
        'status': 'Fan speed succesfully recorded',
        'value': fanValue
         }), 200


@bp.route('/fanSpeed', methods=['GET'])
def get_ac_fan_speed_api():
    fanSpeed = settings.get_ac_fan_speed()
    return jsonify({
        'status': 'Fan speed succesfully retrieved',
        'value': fanSpeed
    }), 200


@bp.route('/health', methods=['GET'])
def get_ac_health_score_api():
    healthScore = settings.get_ac_health_score()
    return jsonify({
        'status': 'Health score succesfully retrieved',
        'value': healthScore
    }), 200


@bp.route('/health', methods=['POST'])
def set_ac_health_score_api():
    json = request.get_json(force=True) 
    healthScore = json['value']
    if not healthScore:
        return jsonify({'status': 'Health score is required.'}), 400

    intHealthScore = int(healthScore)
    if intHealthScore < 1 or intHealthScore > 10:
        return jsonify({'status': 'Health score must be integer between 1 and 10.'}), 400

    healthValue = settings.set_ac_health_score(intHealthScore)
    if intHealthScore < 4:
        settings.set_ac_cleaning_status("START")
        settings.set_ac_power("OFF")
    return jsonify({
        'status': 'Health score succesfully recorded',
        'value': healthValue
         }), 200


@bp.route('/power', methods=['GET'])
def get_ac_power_api():
    power = settings.get_ac_power()
    return jsonify({
        'status': 'AC power succesfully retrieved',
        'value': power
    }), 200


@bp.route('/power', methods=['POST'])
def set_ac_power_api():
    cleaningValue = settings.get_ac_cleaning_status()
    if cleaningValue == 'START':
        return jsonify({'status': 'The device is currently being cleaned and cannot be turned on or off'}), 400
    
    json = request.get_json(force=True) 
    power = json['value']
    if not power:
        return jsonify({'status': 'Power value is required.'}), 400
    if power.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Power must be ON or OFF.'}), 400

    checkTemperature = settings.get_ac_temperature()
    if checkTemperature is None and (power.upper()=="ON"):
        return jsonify({'status': 'You must set a temperature value before turning the device on'}), 400
        
    return settings.set_ac_power(power.upper()), 200
   
    

@bp.route('/light', methods=['GET'])
def get_ac_light_api():
    light, intensity = settings.get_ac_light()
    return jsonify({
        'status': 'Light value succesfully retrieved',
        'value': light,
        "intensity": intensity
    }), 200


@bp.route('/light', methods=['POST'])
def set_ac_light_api():
    currentLightValue, currentIntensity = settings.get_ac_light()
    json = request.get_json(force=True) 
    light = json['value']

    if light is None:
        return jsonify({'status': 'Light value is required.'}), 400
    
    if light.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Light must be ON or OFF.'}), 400

    lightIntensity = 0
    if light == "ON":
        lightIntensityInput = int(json['intensity'])
        if not lightIntensityInput:
            return jsonify({'status': 'Intensity is required if you want to turn the light on.'}), 400
        if lightIntensityInput < 1 or lightIntensityInput > 100:
            return jsonify({'status': 'Light intensity must be integer between 1 and 100.'}), 400
        lightIntensity = lightIntensityInput

    return settings.set_ac_light(light.upper(), lightIntensity), 200


@bp.route('/sound', methods=['GET'])
def get_ac_sound_api():
    sound, volume = settings.get_ac_sound()
    return jsonify({
        'status': 'Sound value succesfully retrieved',
        'value': sound,
        'volume': volume
    }), 200


@bp.route('/sound', methods=['POST'])
def set_ac_sound_api():
    currentSoundValue, currentVolume = settings.get_ac_sound()
    json = request.get_json(force=True) 
    sound = json['value']

    if sound is None:
        return jsonify({'status': 'Sound value is required.'}), 400

    if sound.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Sound must be ON or OFF.'}), 400

    volume = 0
    if sound == "ON":
        volumeInput = int(json['volume'])
        if not volumeInput:
            return jsonify({'status': 'Volume is required if you want to turn the sound on.'}), 400
        if volumeInput < 1 or volumeInput > 100:
            return jsonify({'status': 'Sound volume must be integer between 1 and 100.'}), 400
        volume = volumeInput

    return settings.set_ac_sound(sound.upper(), volume), 200



@bp.route('/cleaning', methods=['GET'])
def get_ac_cleaning_status_api():
    cleaning = settings.get_ac_cleaning_status()
    return jsonify({
        'status': 'Cleaning value succesfully retrieved',
        'value': cleaning
    }), 200


@bp.route('/cleaning', methods=['POST'])
def set_ac_cleaning_status_api():
    json = request.get_json(force=True) 
    cleaning = json['value']
    if not cleaning:
        return jsonify({'status': 'Cleaning value is required.'}), 400
    if cleaning.upper() not in ["START", "STOP"]:
        return jsonify({'status': 'Cleaning value must be START or STOP.'}), 400
    return settings.set_ac_cleaning_status(cleaning.upper()), 200
