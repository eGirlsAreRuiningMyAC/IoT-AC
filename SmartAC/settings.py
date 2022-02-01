from flask import jsonify
from database import get_db


def set_ac_temperature(temperature):
    db = get_db()
    db.execute("INSERT INTO temperature (value) VALUES (?)", (temperature,))
    db.commit()

    check = (
        get_db()
        .execute("SELECT id, timestamp, value FROM temperature ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["value"]


def get_ac_temperature():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value FROM temperature ORDER BY timestamp DESC")
        .fetchone()
    )
    if check is None:
        return None
    return check["value"]


def set_ac_mode(mode):
    db = get_db()
    db.execute("INSERT INTO mode (type) VALUES (?)", (mode.upper(),))
    db.commit()

    check = (
        get_db()
        .execute("SELECT id, timestamp, type FROM mode ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["type"]


def get_ac_mode():
    check = (
        get_db()
        .execute("SELECT id, timestamp, type FROM mode ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["type"]


def set_ac_fan_speed(fanSpeed):
    db = get_db()
    db.execute("INSERT INTO fanSpeed (value) VALUES (?)", (fanSpeed.upper(),))
    db.commit()

    check = db.execute(
        "SELECT id, timestamp, value FROM fanSpeed ORDER BY timestamp DESC"
    ).fetchone()
    return check["value"]


def get_ac_fan_speed():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value FROM fanSpeed ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["value"]


def get_ac_health_score():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value FROM health ORDER BY timestamp DESC")
        .fetchone()
    )
    if check is None:
        return None
    return check["value"]


def set_ac_health_score(intHealthScore):
    db = get_db()
    db.execute("INSERT INTO health (value) VALUES (?)", (intHealthScore,))
    db.commit()

    check = db.execute(
        "SELECT id, timestamp, value FROM health ORDER BY timestamp DESC"
    ).fetchone()
    return check["value"]


def get_ac_power():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value FROM powerStatus ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["value"]


def set_ac_power(power):
    setTurnOn = power.upper() == "ON"
    isAlreadyTurnedOn = get_ac_power() == "ON"

    if isAlreadyTurnedOn == setTurnOn:
        if isAlreadyTurnedOn:
            return {"status": "The air conditioning is already turned on"}
        else:
            return {"status": "The air conditioning is already turned off"}
    else:
        db = get_db()
        db.execute("INSERT INTO powerStatus (value) VALUES (?)", (power.upper(),))
        db.commit()
        if setTurnOn:
            return jsonify({"status": "The air conditioning has been turned on."})
        else:
            return jsonify({"status": "The air conditioning has been turned off."})


def get_ac_light():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value, intensity FROM light ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["value"], check["intensity"]



def set_ac_light_auto(intensity):
    lightValue, lightIntensity = get_ac_light()
    if lightValue == "ON" and get_ac_mode=="AUTO":
        set_ac_light("ON", intensity)


def set_ac_light(light, intensity):
    setTurnOn = light.upper() == "ON"
    currentLightValue, currentIntensity = get_ac_light()
    isAlreadyTurnedOn = currentLightValue == "ON"

    db = get_db()

    if isAlreadyTurnedOn == setTurnOn:
        if isAlreadyTurnedOn:
            db.execute("INSERT INTO light (value, intensity) VALUES (?, ?)", (light.upper(), intensity))
            db.commit()
            return jsonify({"status": "Light is now on with intensity " + str(intensity)})
        else:
            return jsonify({"status": "The light is already turned off."})
    else:
        db.execute("INSERT INTO light (value, intensity) VALUES (?, ?)", (light.upper(), intensity))
        db.commit()
        if setTurnOn:
            return jsonify({"status": "Light is now on with intensity " + str(intensity)})
        else:
            return jsonify({"status": "Light is now off"})


def update_light_auto(envLightIntensity):
    """
    -> update AC light intensity based on env light intensity 
        if mode = auto and light is ON
    acLight = 100 - envLight
    """
    acLightIntensity = 100 - envLightIntensity
    currentACMode = get_ac_mode()
    lightValue, lightIntensity = get_ac_light()
    if currentACMode.upper() == "AUTO" and lightValue.upper() == "ON":
        set_ac_light("ON", acLightIntensity)



def get_ac_sound():
    check = (
        get_db()
        .execute("SELECT id, timestamp, value, volume FROM sound ORDER BY timestamp DESC")
        .fetchone()
    )
    return check["value"], check["volume"]


def set_ac_sound_auto(volume):
    soundValue, soundVolume = get_ac_sound()
    if soundValue == "ON" and get_ac_mode == "AUTO":
        set_ac_sound("ON", volume)


def set_ac_sound(sound, volume):
    setTurnOn = sound.upper() == "ON"
    currentSoundValue, currentVolume = get_ac_sound()
    isAlreadyTurnedOn = currentSoundValue == "ON"

    db = get_db()

    if isAlreadyTurnedOn == setTurnOn:
        if isAlreadyTurnedOn:
            db.execute("INSERT INTO sound (value, volume) VALUES (?, ?)", (sound.upper(), volume))
            db.commit()
            return jsonify({"status": "Sound is now on with volume " + str(volume)})
        else:
            return jsonify({"status": "The sound is already turned off."})
    else:
        db.execute("INSERT INTO sound (value, volume) VALUES (?, ?)", (sound.upper(), volume))
        db.commit()
        if setTurnOn:
            return jsonify({"status": "Sound is now on with volume " + str(volume)})
        else:
            return jsonify({"status": "Sound is now off"})


def update_sound_auto(envSoundVolume):
    """
    -> update AC sound volume based on env sound volume 
        if mode = auto and sound is ON
    acSound = envSound
    """
    currentACMode = get_ac_mode()
    soundValue, soundVolume = get_ac_sound()
    if currentACMode.upper() == "AUTO" and soundValue.upper() == "ON":
        set_ac_sound("ON", envSoundVolume)


def get_ac_cleaning_status():
    check = (
        get_db()
        .execute(
            "SELECT id, cleaning_date, value FROM cleaning ORDER BY cleaning_date DESC"
        )
        .fetchone()
    )
    return check["value"]


def get_cleaning_history():
    cleanings = (
        get_db()
        .execute(
            "SELECT id, cleaning_date, value FROM cleaning ORDER BY cleaning_date DESC"
        )
        .fetchall()
    )

    if cleanings is None:
        return None

    cleaningHistory = []
    for cleaning in cleanings:
        cleaningHistory.append({
            "cleaning_date":cleaning[1],
            "value":cleaning[2]
        })

    return cleaningHistory





def set_ac_cleaning_status(cleaning):
    startCleaning = cleaning.upper() == "START"
    isInCleaning = get_ac_cleaning_status() == "START"
    db = get_db()

    if isInCleaning:
        if startCleaning:
            return jsonify({"status": "The device is currently being cleaned."})
        else:
            set_ac_health_score(10)
            return set_ac_cleaning(cleaning.upper())
    else:
        if not startCleaning:
            return jsonify({"status": "The device is currently not being cleaned."})
        else:
            set_ac_power("OFF")
            return set_ac_cleaning(cleaning.upper())


def set_ac_cleaning(cleaning):
    db = get_db()
    db.execute("INSERT INTO cleaning (value) VALUES (?)", (cleaning.upper(),))
    db.commit()
    return jsonify({"status": "Cleaning value succesfully recorded"})
