from flask import Blueprint, request, jsonify, session
from pyparsing import dblSlashComment
from database import get_db
from auth import login_required

bp = Blueprint('schedule', __name__)


@bp.route('/schedule',methods=['POST'])
@login_required
def add_schedule():
    json = request.get_json(force=True) 
    turnOnTime = json['turnOnTime']
    if not turnOnTime:
        return jsonify({'status': 'Turn on time is required.'}), 400

    turnOffTime = json['turnOffTime']
    if not turnOffTime:
        return jsonify({'status': 'Turn off time is required.'}), 400

    preferenceId = int(json['preferenceId'])
    if not preferenceId:
        return jsonify({'status': 'Preference ID for this schedule is required.'}), 400

    
    userId = session.get('user_id')
    db = get_db()

    checkIfPreferenceExists = db.execute(
        'SELECT id FROM preference WHERE id=(?)',
        (preferenceId,)
    ).fetchone()
    if checkIfPreferenceExists is None:
        return jsonify({'status': 'No preference with this id.'}), 400

    checkUser = db.execute(
        'SELECT id, author_id FROM preference WHERE author_id=(?) AND id=(?)',
        (userId, preferenceId)
    ).fetchone()
    if checkUser is None:
        return jsonify({'status': 'You are not allowed to use this preference'}), 400
    else:
        db.execute(
            'INSERT INTO schedule (author_id, preference_id, turnOnTime, turnOffTime)'
            ' VALUES (?, ?, ?, ?)',
            (userId, preferenceId, turnOnTime, turnOffTime)
        )
        db.commit()
        return jsonify({'status': 'Schedule addded.'}), 200
  


@bp.route('/schedule', methods=['GET'])
@login_required
def get_all_schedules():
    userId = session.get('user_id')
    schedules = get_db().execute(
        'SELECT id, preference_id, turnOnTime, turnOffTime'
        ' FROM schedule WHERE author_id = (?)',
        (userId,)
    ).fetchall()

    if schedules is None:
        return {'status': 'You have no schedule added for the device'}, 200

    schedulesDict = dict()
    for schedule in schedules:
        schedulesDict[schedule[0]]= {
            "preferenceId":schedule[1],
            "turnOnTime":schedule[2],
            "turnOffTime":schedule[3]
        }

    return jsonify({
        'status': 'These are all your schedules',
        'data': schedulesDict
        }), 200


@bp.route('/schedule', methods=['DELETE'])
@login_required
def delete_schedule():
    json = request.get_json(force=True) 
    scheduleId = int(json['id'])
    if not scheduleId:
        return jsonify({'status': 'Schedule ID to be deleted is required.'}), 400

    db = get_db()
    checkIfScheduleExists = db.execute(
        'SELECT id FROM schedule WHERE id=(?)',
        (scheduleId,)
    ).fetchone()
    if checkIfScheduleExists is None:
        return jsonify({'status': 'No schedule with this id'}), 400

    userId = session.get('user_id')
    checkUser = db.execute(
        'SELECT id, author_id FROM schedule WHERE author_id=(?) AND id=(?)',
        (userId, scheduleId)
    ).fetchone()
    if checkUser is None:
        return jsonify({'status': 'You are not allowed to delete this schedule'}), 400
    else:
        db.execute(
            'DELETE FROM schedule WHERE id=(?)',
            (scheduleId,)
        )
        db.commit()
        return jsonify({'status': 'Schedule deleted.'}), 200