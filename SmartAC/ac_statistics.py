from flask import session
from database import get_db

def get_all_statistics():
    users = get_db().execute(
        'SELECT id FROM user'
    ).fetchall()
    statisticsDict = []
    for user in users:
        userId = user["id"]
        stats = get_statistics(userId)["statistics"]
        statisticsDict.append({
            "userId": userId, 
            'temperature': stats["temperature"],
            'light': stats['light'],
            'sound': stats['sound'],
            'mode': stats['mode'],
            'preference': stats["preference"]
        })
    return statisticsDict


def get_statistics_current_user():
    userId = session.get('user_id')
    return get_statistics(userId)


def get_statistics(userId):
    # preponderent light on sau off
    # preponderent sound on sau off
    # temperatura medie
    # cea mai utilizata preferinta a utilizatorului
    # cel mai utilizat mod

    db = get_db()

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

    preferenceValue = None if (preference is None) else preference["preference_id"]

    return {
        'statistics': {
            'temperature': temperature["avgValue"],
            'light': light['value'],
            'sound': sound['value'],
            'mode': mode['type'],
            'preference': preferenceValue
        }
    }