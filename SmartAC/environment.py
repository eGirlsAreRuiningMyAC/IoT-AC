from flask import Blueprint, request, jsonify
from database import get_db
from auth import login_required

bp = Blueprint('environment', __name__, url_prefix='/air')


@bp.route('/temperature', methods=['POST'])
@login_required
def set_air_temperature_api():
    json = request.get_json(force=True) 
    airTemperature = json['value']
    if not airTemperature:
        return jsonify({'status': 'Air temperature is required.'}), 400
    return set_air_temperature(airTemperature), 200


def set_air_temperature(airTemperature):
    db = get_db()
    db.execute(
        'INSERT INTO airTemperature (value) VALUES (?)',
        (airTemperature,)
    )
    db.commit()

    """
    -> update temperature of AC if mode = auto
    <0 : 27, 0 - 10: 25, 10-20: 23, 20-30: 21, 30+: 19
    """
    currentACMode = db.execute(
        'SELECT timestamp, type FROM mode ORDER BY timestamp DESC'
    ).fetchone()["type"]

    if currentACMode.upper() =="AUTO":
        updatedACTemperature = 27
        if airTemperature >0:
            updatedACTemperature -=2
        if airTemperature >10:
            updatedACTemperature -=2
        if airTemperature >20:
            updatedACTemperature -=2
        if airTemperature >30:
            updatedACTemperature -=2

        db.execute(
            'INSERT INTO temperature (value) VALUES (?)',
            (updatedACTemperature,)
        )
        db.commit()

    check = db.execute(
        'SELECT timestamp, value FROM airTemperature ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'Air emperature succesfully recorded',
        'value': check['value']
        })



@bp.route('/temperature', methods=['GET'])
def get_air_temperature():
    airTemperature = get_db().execute(
        'SELECT timestamp, value FROM airTemperature ORDER BY timestamp DESC'
    ).fetchone()
    if airTemperature is None:
        return {'status': 'Please set a value for air temperature'}, 200
    return jsonify({
        'status': 'Air temperature succesfully retrieved',
        'value': airTemperature['value']
        }), 200



@bp.route('/humidity', methods=['POST'])
@login_required
def set_air_humidity_api():
    json = request.get_json(force=True) 
    humidity = json['value']
    if not humidity:
        return jsonify({'status': 'Air humidity is required.'}), 400
    return set_air_humidity(humidity), 200


def set_air_humidity(humidity):
    db = get_db()
    db.execute(
        'INSERT INTO airHumidity (value) VALUES (?)',
        (humidity,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT timestamp, value FROM airHumidity ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Air humidity succesfully recorded',
        'value': check['value']
        })



@bp.route('/humidity', methods=['GET'])
def get_air_humidity():
    airHumidity = get_db().execute(
        'SELECT timestamp, value FROM airHumidity ORDER BY timestamp DESC'
    ).fetchone()
    if airHumidity is None:
        return {'status': 'Please set a value for air humidity'}, 200
    return jsonify({
        'status': 'Air humidity succesfully retrieved',
        'value': airHumidity['value']
        }), 200