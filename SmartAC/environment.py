from database import get_db


def set_air_temperature(airTemperature):
    db = get_db()
    db.execute("INSERT INTO airTemperature (value) VALUES (?)", (airTemperature,))
    db.commit()
    return get_air_temperature()


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
