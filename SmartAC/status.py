from database import get_db

def get_status():
    airHumidity = get_db().execute(
        'SELECT timestamp, value'
        ' FROM airHumidity'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if airHumidity is None:
        return {'status': 'Please set a value for air humidity'}

    powerState  = get_db().execute(
        'SELECT timestamp, value'
        ' FROM powerStatus'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if powerState is None:
        return {'status': 'Please set a value for power (ON or OFF)'}



    airTemperature = get_db().execute(
        'SELECT timestamp, value'
        ' FROM airTemperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if airTemperature is None:
        return {'status': 'Please set a value for air temperature'}
   

    temperature = get_db().execute(
        'SELECT timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if temperature is None:
        return {'status': 'Please set a value for temperature'}


    mode = get_db().execute(
        'SELECT timestamp, type'
        ' FROM mode'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if mode is None:
        return {'status': 'Please set a value for mode (auto, cool, dry, fan, heat, eco)'}

   
    fanSpeed = get_db().execute(
        'SELECT timestamp, value'
        ' FROM fanSpeed'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if fanSpeed is None:
        return {'status': 'Please set a value for fan speed (low, medium, high)'}


    healthScore = get_db().execute(
        'SELECT timestamp, value'
        ' FROM health'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if healthScore is None:
        return {'status': 'Please set a score for device health'}


    cleaning = get_db().execute(
        'SELECT timestamp, value'
        ' FROM cleaning'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    light = get_db().execute(
        'SELECT timestamp, value'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    sound = get_db().execute(
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