from flask import Blueprint, request, jsonify
from database import get_db
from auth import login_required

bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/temperature', methods=['POST'])
@login_required
def set_ac_temperature():
    json = request.get_json(force=True) 
    temperature = json['value']
    if not temperature:
        return jsonify({'status': 'Temperature is required.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO temperature (value) VALUES (?)',
        (temperature,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, value FROM temperature ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Temperature succesfully recorded',
        'value': check['value']
         }), 200


@bp.route('/temperature', methods=['GET'])
def get_ac_temperature():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM temperature ORDER BY timestamp DESC'
    ).fetchone()
    if check is None:
        return jsonify({
        'status': 'Please set a value for temperature',
        'value': "None"
        }), 200
    return jsonify({
        'status': 'Temperature succesfully retrieved',
        'value': check['value']
        }), 200



@bp.route('/mode', methods=['POST'])
@login_required
def set_ac_mode():
    json = request.get_json(force=True) 
    mode = json['value']
    if not mode:
        return jsonify({'status': 'Mode is required.'}), 400
    if mode.upper() not in ["AUTO", "COOL", "DRY", "FAN", "HEAT", "ECO"]:
        return jsonify({'status': 'Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO mode (type) VALUES (?)',
        (mode.upper(),)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, type FROM mode ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Mode succesfully recorded',
        'value': check['type']
        }), 200


@bp.route('/mode', methods=['GET'])
def get_ac_mode():
    check = get_db().execute(
        'SELECT id, timestamp, type FROM mode ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Mode succesfully retrieved',
        'value': check['type']
        }), 200



@bp.route('/fanSpeed', methods=['POST'])
@login_required
def set_ac_fan_speed():
    json = request.get_json(force=True) 
    fanSpeed = json['value']
    if not fanSpeed:
        return jsonify({'status': 'Fan speed is required.'}), 400
    if fanSpeed.upper() not in ["LOW", "MEDIUM", "HIGH"]:
        return jsonify({'status': 'Fan speed must be LOW, MEDIUM or HIGH.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO fanSpeed (value) VALUES (?)',
        (fanSpeed.upper(),)
    )
    db.commit()

    check = db.execute(
        'SELECT id, timestamp, value FROM fanSpeed ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Fan speed succesfully recorded',
        'value': check['value']
        }), 200


@bp.route('/fanSpeed', methods=['GET'])
def get_ac_fan_speed():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM fanSpeed ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Fan speed succesfully retrieved',
        'value': check['value']
        }), 200



@bp.route('/health', methods=['GET'])
def get_ac_health_score():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM health ORDER BY timestamp DESC'
    ).fetchone()
    if check is None:
        return {'status': 'No health score for this device'}, 200
    return jsonify({
        'status': 'Health succesfully retrieved',
        'value': check['value']
        }), 200


@bp.route('/health', methods=['POST'])
@login_required
def set_ac_health_score():
    json = request.get_json(force=True) 
    healthScore = json['value']
    if not healthScore:
        return jsonify({'status': 'Health score is required.'}), 400

    intHealthScore = int(healthScore)
    if intHealthScore<1 or intHealthScore>10:
        return jsonify({'status': 'Health score must be between 1 and 10.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO health (value) VALUES (?)',
        (intHealthScore,)
    )
    db.commit()
    if intHealthScore < 4:
        db.execute(
            'INSERT INTO cleaning (value) VALUES (?)',
            ("START",)
        )
        db.commit()
        db.execute(
            'INSERT INTO powerStatus (value) VALUES (?)',
            ("OFF",)
        )
        db.commit()

    check = db.execute(
        'SELECT id, timestamp, value FROM health ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Health score succesfully recorded',
        'value': check['value']
        }), 200



@bp.route('/power', methods=['GET'])
def get_ac_power():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM powerStatus ORDER BY timestamp DESC'
    ).fetchone()
    isTurnedOn = check['value']
    if isTurnedOn=="ON":
        return jsonify({
            'status': 'The ac is ON',
            'value': isTurnedOn
            }), 200
    else: 
        return jsonify({
            'status': 'The ac is OFF',
            'value': isTurnedOn
            }), 200

  
@bp.route('/power', methods=['POST'])
@login_required
def set_ac_power():
    checkCleaning = get_db().execute(
        'SELECT id, cleaning_date, value FROM cleaning ORDER BY cleaning_date DESC'
    ).fetchone()
    if checkCleaning["value"]=='START':
        return jsonify({'status': 'The device is currently being cleaned and cannot be turned on or off'}), 400

    json = request.get_json(force=True) 
    power = json['value']
    if not power:
        return jsonify({'status': 'Power value is required.'}), 400

    if power.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Power must be ON or OFF.'}), 400

    setTurnOn = power.upper()=="ON"
    db = get_db()

    checkTemperature = get_db().execute(
        'SELECT id timestamp, value FROM temperature ORDER BY timestamp DESC'
    ).fetchone()
    if checkTemperature is None and setTurnOn:
        return jsonify({'status': 'You must set a temperature value before turning the device on'}), 400


    check = db.execute(
        'SELECT id, timestamp, value FROM powerStatus ORDER BY timestamp DESC'
    ).fetchone()
    isAlreadyTurnedOn = check['value']=="ON"

    if isAlreadyTurnedOn==setTurnOn:
        if isAlreadyTurnedOn:
            return {'status': 'The air conditioning is already turned on'}, 200
        else:
            return {'status': 'The air conditioning is already turned off'}, 200
    else:
        db.execute(
            'INSERT INTO powerStatus (value) VALUES (?)',
            (power.upper(),)
        )
        db.commit()
        if setTurnOn:
            return jsonify({'status': 'The air conditioning has been turned on.'}), 200
        else:
            return jsonify({'status': 'The air conditioning has been turned off.'}), 200



@bp.route('/light', methods=['GET'])
def get_ac_light():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM light ORDER BY timestamp DESC'
    ).fetchone()
    
    return jsonify({
        'status': 'Light value succesfully retrieved',
        'value': check['value']
        }), 200
      

@bp.route('/light', methods=['POST'])
@login_required
def set_ac_light():
    json = request.get_json(force=True) 
    light = json['value']
    if not light:
        return jsonify({'status': 'Lght value is required.'}), 400
    if light.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Light must be ON or OFF.'}), 400

    setTurnOn = light.upper()=="ON"
    db = get_db()

    check = db.execute(
        'SELECT id, timestamp, value FROM light ORDER BY timestamp DESC'
    ).fetchone()
    isAlreadyTurnedOn = check['value']=="ON"

    if isAlreadyTurnedOn==setTurnOn:
        if isAlreadyTurnedOn:
            return jsonify({'status': 'The light is already turned on.'}), 200
        else:
            return jsonify({'status': 'The light is already turned off.'}), 200
    else:
        db.execute(
            'INSERT INTO light (value) VALUES (?)',
            (light.upper(),)
        )
        db.commit()
        if setTurnOn:
            return jsonify({'status': 'Light is not on'}), 200
        else:
            return jsonify({'status': 'Light is not off'}), 200



@bp.route('/sound', methods=['GET'])
def get_ac_sound():
    check = get_db().execute(
        'SELECT id, timestamp, value FROM sound ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Sound value succesfully retrieved',
        'value': check['value']
        }), 200


@bp.route('/sound', methods=['POST'])
@login_required
def set_ac_sound():
    json = request.get_json(force=True) 
    sound = json['value']
    if not sound:
        return jsonify({'status': 'Sound value is required.'}), 400
    if sound.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Sound must be ON or OFF.'}), 400

    setTurnOn = sound.upper()=="ON"
    db = get_db()

    check = db.execute(
        'SELECT id, timestamp, value FROM sound ORDER BY timestamp DESC'
    ).fetchone()
    isAlreadyTurnedOn = check['value']=="ON"

    if isAlreadyTurnedOn==setTurnOn:
        if isAlreadyTurnedOn:
            return jsonify({'status': 'The sound is already turned on.'}), 200
        else:
            return jsonify({'status': 'The sound is already turned off.'}), 200
    else:
        db.execute(
            'INSERT INTO sound (value) VALUES (?)',
            (sound.upper(),)
        )
        db.commit()
        if setTurnOn:
            return jsonify({'status': 'Sound is not on'}), 200
        else:
            return jsonify({'status': 'Sound is not off'}), 200




@bp.route('/cleaning', methods=['GET'])
def get_ac_cleaning_status():
    check = get_db().execute(
        'SELECT id, cleaning_date, value FROM cleaning ORDER BY cleaning_date DESC'
    ).fetchone()
    return jsonify({
        'status': 'Cleaning value succesfully retrieved',
        'value': check['value']
        }), 200


@bp.route('/cleaning', methods=['POST'])
@login_required
def set_ac_cleaning_status():
    json = request.get_json(force=True) 
    cleaning = json['cleaning']
    if not cleaning:
        return jsonify({'status': 'Cleaning value is required.'}), 400
    if cleaning.upper() not in ["START", "STOP"]:
        return jsonify({'status': 'Cleaning value must be START or STOP.'}), 400

    startCleaning = cleaning.upper()=="START"
    db = get_db()

    check = db.execute(
        'SELECT id, cleaning_date, value FROM cleaning ORDER BY cleaning_date DESC'
    ).fetchone()
    isInCleaning = check['value']=="START"

    if isInCleaning:
        if startCleaning:
            return jsonify({'status': 'The device is currently being cleaned.'}), 200
        else:
            db.execute(
                'INSERT INTO cleaning (value) VALUES (?)',
                (cleaning.upper(),)
            )
            db.commit()
            db.execute(
                'INSERT INTO health (value) VALUES (?)',
                (10,)
            )
            db.commit()
            
            return jsonify({'status': 'Cleaning value succesfully recorded'}), 200
    else:
        if not startCleaning:
            return jsonify({'status': 'The device is currently not being cleaned.'}), 200
        else:
            db.execute(
                'INSERT INTO cleaning (value) VALUES (?)',
                (cleaning.upper(),)
            )
            db.commit()
            db.execute(
                'INSERT INTO powerStatus (value) VALUES (?)',
                ("OFF",)
            )
            db.commit()
            return jsonify({'status': 'Cleaning value succesfully recorded'}), 200
        