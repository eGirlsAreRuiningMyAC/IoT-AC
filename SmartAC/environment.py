from database import get_db
import settings

def set_air_temperature(airTemperature):
    db = get_db()
    db.execute("INSERT INTO airTemperature (value) VALUES (?)", (airTemperature,))
    db.commit()
    return get_air_temperature()


def update_temperature_auto(airTemperature):
    """
    -> update temperature of AC if mode = auto
    <0 : 27, 0 - 10: 25, 10-20: 23, 20-30: 21, 30+: 19
    """
    currentACMode = settings.get_ac_mode()
    if currentACMode.upper() == "AUTO":
        updatedACTemperature = 27
        if airTemperature >0:
            updatedACTemperature -=2
        if airTemperature >10:
            updatedACTemperature -=2
        if airTemperature >20:
            updatedACTemperature -=2
        if airTemperature >30:
            updatedACTemperature -=2
        settings.set_ac_temperature(updatedACTemperature)
        

def get_air_temperature():
    airTemperature = (
        get_db()
        .execute("SELECT timestamp, value FROM airTemperature ORDER BY timestamp DESC")
        .fetchone()
    )
    if airTemperature is None:
        return None
    else:
        return airTemperature["value"]



def set_air_humidity(humidity):
    db = get_db()
    db.execute("INSERT INTO airHumidity (value) VALUES (?)", (humidity,))
    db.commit()
    return get_air_humidity()


def get_air_humidity():
    airHumidity = (
        get_db()
        .execute("SELECT timestamp, value FROM airHumidity ORDER BY timestamp DESC")
        .fetchone()
    )
    if airHumidity is None:
        return None
    else:
        return airHumidity["value"]
