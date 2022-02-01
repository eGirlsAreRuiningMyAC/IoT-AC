from flask import Blueprint, jsonify, request
from auth import login_required
import preference
import schedule

bp = Blueprint('schedule', __name__)

@bp.route('/schedule',methods=['POST'])
@login_required
def add_schedule_api():
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

    preferenceExists = preference.checkIfPreferenceExists(preferenceId)
    if preferenceExists:
        preferenceForCurrentUser = preference.checkIfPreferenceIsForUser(preferenceId)
        if preferenceForCurrentUser:
            schedule.add_schedule(turnOnTime, turnOffTime, preferenceId)
            return jsonify({'status': 'Schedule addded.'}), 200
        else:
            return jsonify({'status': 'You are not allowed to user this preference'}), 400

    else:
        return jsonify({'status': 'No preference with this id.'}), 400


@bp.route('/schedule', methods=['GET'])
@login_required
def get_all_schedules_api():
    schedules = schedule.get_all_schedules()
    return jsonify({
        'status': 'These are all your schedules',
        'schedules': schedules
        }), 200

@bp.route('/schedule', methods=['DELETE'])
@login_required
def delete_schedule_api():
    json = request.get_json(force=True) 
    scheduleId = int(json['id'])
    if not scheduleId:
        return jsonify({'status': 'Schedule ID to be deleted is required.'}), 400
    
    scheduleExists = schedule.checkIfScheduleExists(scheduleId)
    if scheduleExists:
        scheduleForCurrentUser = schedule.checkIfScheduleIsForUser(scheduleId)
        if scheduleForCurrentUser:
            schedule.delete_schedule(scheduleId)
            return jsonify({'status': 'Schedule deleted.'}), 200
        else:
            return jsonify({'status': 'You are not allowed to delete this schedule'}), 400

    else:
        return jsonify({'status': 'No schedule with this id.'}), 400