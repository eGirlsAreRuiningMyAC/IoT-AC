from flask import jsonify, session
from database import get_db


def add_schedule(turnOnTime, turnOffTime, preferenceId):
    userId = session.get('user_id')
    db = get_db() 

    db.execute(
        'INSERT INTO schedule (author_id, preference_id, turnOnTime, turnOffTime)'
        ' VALUES (?, ?, ?, ?)',
        (userId, preferenceId, turnOnTime, turnOffTime)
    )
    db.commit()
  


def get_all_schedules():
    userId = session.get('user_id')
    schedules = get_db().execute(
        'SELECT id, preference_id, turnOnTime, turnOffTime'
        ' FROM schedule WHERE author_id = (?)',
        (userId,)
    ).fetchall()

    if schedules is None:
        return None

    schedulesDict = dict()
    for schedule in schedules:
        schedulesDict[schedule[0]]= {
            "preferenceId":schedule[1],
            "turnOnTime":schedule[2],
            "turnOffTime":schedule[3]
        }

    return schedulesDict



def checkIfScheduleExists(scheduleId):
    checkIfScheduleExists = get_db().execute(
       'SELECT id FROM schedule WHERE id=(?)',
        (scheduleId,)
    ).fetchone()
    if checkIfScheduleExists is None:
        return False
    return True


def checkIfScheduleIsForUser(scheduleId):
    userId = session.get('user_id')
    checkUser = get_db().execute(
        'SELECT id, author_id FROM schedule WHERE author_id=(?) AND id=(?)',
        (userId, scheduleId)
    ).fetchone()
    if checkUser is None:
        return False
    return True


def delete_schedule(scheduleId):
    db = get_db()
    db.execute(
        'DELETE FROM schedule WHERE id=(?)',
        (scheduleId,)
    )
    db.commit()