from flask import Blueprint, request, jsonify, session
from database import get_db
from auth import login_required

bp = Blueprint('preference', __name__)


@bp.route('/preference',methods=['POST'])
@login_required
def add_preference():
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
    
    userId = session.get('user_id')
    db = get_db()
    db.execute(
        'INSERT INTO preference (author_id, temperature, mode, fanSpeed, light, sound)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (userId, temperature, mode.upper(), fanSpeed.upper(), light.upper(), sound.upper())
    )
    db.commit()
    return jsonify({'status': 'Preference addded.'}), 200
  



@bp.route('/preference', methods=['GET'])
@login_required
def get_all_preferences():
    userId = session.get('user_id')
    preferences = get_db().execute(
        'SELECT id, temperature, mode, fanSpeed, light, sound'
        ' FROM preference'
        ' WHERE author_id = (?)',
        (userId,)
    ).fetchall()

    if preferences is None:
        return {'status': 'You have no prefences added for the device'}, 200

    preferencesDict = dict()
    for preference in preferences:
        preferencesDict[preference[0]]= {
            "temperature":preference[1],
            "mode":preference[2],
            "fanSpeed":preference[3],
            "light":preference[4],
            "sound":preference[5]
        }

    return jsonify({
        'status': 'These are all your preferences',
        'data': preferencesDict
        }), 200


@bp.route('/preference', methods=['DELETE'])
@login_required
def delete_preference():
    json = request.get_json(force=True) 
    preferenceId = int(json['id'])
    if not preferenceId:
        return jsonify({'status': 'Preference ID to be deleted is required.'}), 400

    db = get_db()
    checkIfPreferenceExists = db.execute(
       'SELECT id FROM preference WHERE id=(?)',
        (preferenceId,)
    ).fetchone()
   
    if checkIfPreferenceExists is None:
        return jsonify({'status': 'No preference with this id.'}), 400

    userId = session.get('user_id')
    checkUser = db.execute(
        'SELECT id, author_id FROM preference WHERE author_id=(?) AND id=(?)',
        (userId, preferenceId)
    ).fetchone()
    if checkUser is None:
        return jsonify({'status': 'You are not allowed to delete this preference'}), 400
    else:
        db.execute(
            'DELETE FROM preference WHERE id=(?)',
            (preferenceId,)
        )
        db.commit()
        return jsonify({'status': 'Preference deleted.'}), 200