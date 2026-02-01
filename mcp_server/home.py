def format_temp(data):
    return f"{round(float(data))}"


def format_humi(data):
    return f"{round(float(data))}"


def get_value(room, data):
    if room is not None and data in room:
        if data == 'temp':
            return format_temp(room[data])
        if data == 'humi':
            return format_humi(room[data])
        if data == 'light':
            return "light" if room[data] else "  "
        if data == 'pir':
            return "movement" if room[data] else "  "
    return "no data"


def home_data(storage):
    kitchen = storage.get("node-kitchen")
    lib = storage.get("node-lib")
    living = storage.get("node-living")
    north = storage.get("node-north")
    toilet = storage.get("node-toilet")

    layout = f"""
    Home data:\n
    - Kitchen:\n
    Temperature: {get_value(kitchen,'temp')}\n
    Humidity: {get_value(kitchen, 'humi')}\n
    Movement: {get_value(kitchen,'pir')}\n
    Light: {get_value(kitchen, 'light')}\n
    - Library / computer room:\n
    Temperature: {get_value(lib,'temp')}\n
    Humidity: {get_value(lib, 'humi')}\n
    Movement: {get_value(lib,'pir')}\n
    Light: {get_value(lib, 'light')}\n
    - Living / main room:\n
    Temperature: {get_value(living,'temp')}\n
    Humidity: {get_value(living, 'humi')}\n
    Movement: {get_value(living,'pir')}\n
    Light: {get_value(living, 'light')}\n
    - North room:\n
    Temperature: {get_value(north,'temp')}\n
    Humidity: {get_value(north, 'humi')}\n
    Movement: {get_value(north,'pir')}\n
    Light: {get_value(north, 'light')}\n   
    - Toilet:\n
    Temperature: {get_value(toilet,'temp')}\n
    Humidity: {get_value(toilet, 'humi')}\n
    Movement: {get_value(toilet,'pir')}\n
    Light: {get_value(toilet, 'light')}\n     
    """

    return layout
