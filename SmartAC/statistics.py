from tkinter import OFF
from webbrowser import get
from flask import Blueprint, request, jsonify, session
from database import get_db
from auth import login_required

bp = Blueprint('statistics', __name__)


@bp.route('/statistics',methods=['GET'])
@login_required
def get_statistics():
    db = get_db()
    userId = session.get('user_id')

    # preponderent light on sau off
    # preponderent sound on sau off
    # temperatura medie
    # cea mai utilizata preferinta a utilizatorului 
    # cel mai utilizat mod

    temperature =db.execute(
        'SELECT AVG(value) AS avgValue'
        ' FROM temperature'
    ).fetchone()

    light = db.execute(
        'SELECT value, COUNT(*) AS lightPreference'
        ' FROM light'
        ' GROUP BY value'
        ' ORDER BY lightPreference DESC'
    ).fetchone()

    sound = db.execute(
        'SELECT value, COUNT(*) AS soundPreference'
        ' FROM sound'
        ' GROUP BY value'
        ' ORDER BY soundPreference DESC'
    ).fetchone()

    mode = db.execute(
        'SELECT type, COUNT(*) AS modePreference'
        ' FROM mode'
        ' GROUP BY type'
        ' ORDER BY modePreference DESC'
    ).fetchone()


    preference = db.execute(
        'SELECT author_id, preference_id, COUNT(*) AS preference'
        ' FROM schedule'
        ' WHERE author_id = (?)'
        ' GROUP BY preference_id'
        ' ORDER BY preference DESC',
        (userId,)
    ).fetchone()

    if temperature is None or temperature["avgValue"] is None:
        temperatureValue = "No temperature for this device yet"
    else:
        temperatureValue = temperature["avgValue"]

    if preference is None:
        preferenceValue = "No preference used for this device yet"
    else:
        preferenceValue = preference["preference_id"]

    return jsonify({
        'status': 'Statistics succesfully retrieved',
        'statistics': {
            'temperature': temperatureValue,
            'light': light['value'],
            'sound': sound['value'],
            'mode': mode['type'],
            'preference': preferenceValue
        }
    }), 200