from flask import  session
from database import get_db
from auth import login_required


def add_preference(temperature, mode, fanSpeed, light, sound):
    userId = session.get('user_id')
    db = get_db()
    db.execute(
        'INSERT INTO preference (author_id, temperature, mode, fanSpeed, light, sound)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (userId, temperature, mode, fanSpeed, light, sound)
    )
    db.commit()
  

def get_all_preferences():
    userId = session.get('user_id')
    preferences = get_db().execute(
        'SELECT id, temperature, mode, fanSpeed, light, sound'
        ' FROM preference'
        ' WHERE author_id = (?)',
        (userId,)
    ).fetchall()

    if preferences is None:
        return None

    preferencesDict = dict()
    for preference in preferences:
        preferencesDict[preference[0]]= {
            "temperature":preference[1],
            "mode":preference[2],
            "fanSpeed":preference[3],
            "light":preference[4],
            "sound":preference[5]
        }

    return preferencesDict



def checkIfPreferenceExists(preferenceId):
    checkIfPreferenceExists = get_db().execute(
       'SELECT id FROM preference WHERE id=(?)',
        (preferenceId,)
    ).fetchone()
    if checkIfPreferenceExists is None:
        return False
    return True


def checkIfPreferenceIsForUser(preferenceId):
    userId = session.get('user_id')
    checkUser = get_db().execute(
        'SELECT id, author_id FROM preference WHERE author_id=(?) AND id=(?)',
        (userId, preferenceId)
    ).fetchone()
    if checkUser is None:
        return False
    return True

def delete_preference(preferenceId):
    db = get_db()
    db.execute(
        'DELETE FROM preference WHERE id=(?)',
        (preferenceId,)
    )
    db.commit()