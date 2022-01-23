from database import get_db

def get_status():
    db = get_db()
    airHumidity = db.execute(
        'SELECT timestamp, value'
        ' FROM airHumidity'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if airHumidity is None:
        return {'status': 'Please set a value for air humidity'}, 200


    powerState  = db.execute(
        'SELECT timestamp, value'
        ' FROM powerStatus'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if powerState is None:
        return {'status': 'Please set a value for power (ON or OFF)'}, 200



    airTemperature = db.execute(
        'SELECT timestamp, value'
        ' FROM airTemperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if airTemperature is None:
        return {'status': 'Please set a value for air temperature'}, 200
   

    temperature = db.execute(
        'SELECT timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if temperature is None:
        return {'status': 'Please set a value for temperature'}, 200



    mode = db.execute(
        'SELECT timestamp, type'
        ' FROM mode'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if mode is None:
        return {'status': 'Please set a value for mode (auto, cool, dry, fan, heat, eco)'}, 200

   

    fanSpeed = db.execute(
        'SELECT timestamp, value'
        ' FROM fanSpeed'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if fanSpeed is None:
        return {'status': 'Please set a value for fan speed (low, medium, high)'}, 200



    healthScore = db.execute(
        'SELECT timestamp, value'
        ' FROM health'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if healthScore is None:
        return {'status': 'Please set a score for device health'}, 200


    cleaning = db.execute(
        'SELECT cleaning_date, value'
        ' FROM cleaning'
        ' ORDER BY cleaning_date DESC'
    ).fetchone()

    light = db.execute(
        'SELECT timestamp, value'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    sound = db.execute(
        'SELECT timestamp, value'
        ' FROM sound'
        ' ORDER BY timestamp DESC'
    ).fetchone()


    return {
        'data': {
            'powerState': powerState['value'],
            'airHumidity': airHumidity['value'],
            'airTemperature': airTemperature['value'],
            'temperature': temperature['value'],
            'mode': mode['type'],
            'fanSpeed': fanSpeed['value'],
            'healthScore': healthScore['value'],
            'cleaning': {
                'value' : cleaning['value'],
                'cleaning_date': cleaning['cleaning_date'],
            },
            'light': light['value'],
            'sound': sound['value']
        }
    }