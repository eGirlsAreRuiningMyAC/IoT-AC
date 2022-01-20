from flask import Blueprint, request, jsonify
from database import get_db
from auth import login_required

bp = Blueprint('environment', __name__, url_prefix='/air')


@bp.route('/temperature', methods=['POST'])
@login_required
def set_air_temperature():
    airTemperature = request.form['airTemperature']
    if not airTemperature:
        return jsonify({'status': 'Air temperature is required.'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO airTemperature (value) VALUES (?)',
        (airTemperature,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT timestamp, value FROM temperature ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'Air emperature succesfully recorded',
        'airTemperature': check['value']
        }), 200



@bp.route('/temperature', methods=['GET'])
def get_air_temperature():
    airTemperature = get_db().execute(
        'SELECT timestamp, value FROM airTemperature ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Air temperature succesfully retrieved',
        'airTemperature': airTemperature['value']
        }), 200


         
@bp.route('/humidity', methods=['POST'])
@login_required
def set_air_humidity():
    humidity = request.form['humidity']
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
        'airHumidity': check['value']
        }), 200



@bp.route('/humidity', methods=['GET'])
def get_air_humidity():
    check = get_db().execute(
        'SELECT timestamp, value FROM airHumidity ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Air humidity succesfully retrieved',
        'airHumidity': check['value']
        }), 200