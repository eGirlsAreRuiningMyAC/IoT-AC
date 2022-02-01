from flask import Blueprint, request, jsonify
from auth import login_required
import preference

bp = Blueprint('preference', __name__)


@bp.route('/preference',methods=['POST'])
@login_required
def add_preference_api():
    json = request.get_json(force=True) 
    temperature = json['temperature']
    if not temperature:
        return jsonify({'status': 'Temperature value is required.'}), 400

    mode = json['mode']
    if not mode:
        return jsonify({'status': 'Mode is required.'}), 400
    if mode.upper() not in ["AUTO", "COOL", "DRY", "FAN", "HEAT", "ECO"]:
        return jsonify({'status': 'Mode must be AUTO, COOL, DRY, FAN, HEAT or ECO.'}), 400

    fanSpeed = json['fanSpeed']
    if not fanSpeed:
        return jsonify({'status': 'Fan speed is required.'}), 400
    if fanSpeed.upper() not in ["LOW", "MEDIUM", "HIGH"]:
        return jsonify({'status': 'Fan speed must be LOW, MEDIUM or HIGH.'}), 400

    light = json['light']
    if not light:
        return jsonify({'status': 'Light value is required.'}), 400
    if light.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Light must be ON or OFF.'}), 400

    sound = json['sound']
    if not sound:
        return jsonify({'status': 'Sound value is required.'}), 400
    if sound.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'Sound must be ON or OFF.'}), 400

    preference.add_preference(temperature, mode.upper(), fanSpeed.upper(), light.upper(), sound.upper())
    return jsonify({'status': 'Preference addded.'}), 200



@bp.route('/preference', methods=['GET'])
@login_required
def get_all_preferences_api():
    preferences = preference.get_all_preferences()
    return jsonify({
        'status': 'These are all your preferences',
        'preferences': preferences
        }), 200


@bp.route('/preference', methods=['DELETE'])
@login_required
def delete_preference_api():
    json = request.get_json(force=True) 
    preferenceId = int(json['id'])
    if not preferenceId:
        return jsonify({'status': 'Preference ID to be deleted is required.'}), 400

    preferenceExists = preference.checkIfPreferenceExists(preferenceId)
    if preferenceExists:
        preferenceForCurrentUser = preference.checkIfPreferenceIsForUser(preferenceId)
        if preferenceForCurrentUser:
            preference.delete_preference(preferenceId)
            return jsonify({'status': 'Preference deleted.'}), 200
        else:
            return jsonify({'status': 'You are not allowed to delete this preference'}), 400

    else:
        return jsonify({'status': 'No preference with this id.'}), 400
