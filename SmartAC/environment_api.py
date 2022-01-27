from flask import Blueprint, request, jsonify
from auth import login_required
import environment as env
import settings

bp = Blueprint('environment', __name__, url_prefix='/air')


@bp.route('/temperature', methods=['POST'])
@login_required
def set_air_temperature_api():
    json = request.get_json(force=True) 
    airTemperature = json['value']
    if not airTemperature:
        return jsonify({'status': 'Air temperature is required.'}), 400
    value = env.set_air_temperature(airTemperature)
    env.update_temperature_auto(airTemperature)

    return jsonify({
        'status': 'Air temperature succesfully recorded',
        'value': value
        }), 200



@bp.route('/humidity', methods=['POST'])
@login_required
def set_air_humidity_api():
    json = request.get_json(force=True) 
    humidity = json['value']
    if not humidity:
        return jsonify({'status': 'Air humidity is required.'}), 400
    value = env.set_air_humidity(humidity)
    return jsonify({
        'status': 'Air humidity succesfully recorded',
        'value': value
        }), 200



@bp.route('/temperature', methods=['GET'])
def get_air_temperature_api():
    airTemperature =  env.get_air_temperature()
    if airTemperature is None:
        return jsonify({
        'status': 'Please set a value for air temperature first',
        'value': airTemperature
        }), 200
    return jsonify({
        'status': 'Air temperature succesfully retrieved',
        'value': airTemperature
        }), 200



@bp.route('/humidity', methods=['GET'])
def get_air_humidity_api():
    airHumidity =  env.get_air_humidity()
    if airHumidity is None:
        return jsonify({
        'status': 'Please set a value for air humidity first',
        'value': airHumidity
        }), 200
    return jsonify({
        'status': 'Air humidity succesfully retrieved',
        'value': airHumidity
        }), 200