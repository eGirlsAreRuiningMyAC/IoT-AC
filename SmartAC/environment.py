from flask import Blueprint, request, jsonify
from database import get_db
from auth import login_required

bp = Blueprint('environment', __name__, url_prefix='/air')


@bp.route('/temperature', methods=['POST'])
@login_required
def set_air_temperature():
    json = request.get_json(force=True) 
    airTemperature = json['value']
  
    if not airTemperature:
        return jsonify({'status': 'Air temperature is required.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO airTemperature (value) VALUES (?)',
        (airTemperature,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT timestamp, value FROM airTemperature ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'Air emperature succesfully recorded',
        'value': check['value']
        }), 200



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
def set_air_humidity():
    json = request.get_json(force=True) 
    humidity = json['value']

    if not humidity:
        return jsonify({'status': 'Air humidity is required.'}), 400

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
        }), 200



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