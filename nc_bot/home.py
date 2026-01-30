
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
            return "💡" if room[data] else "  "
        if data == 'pir':
            return "🙋" if room[data] else "  "
    return "--"


def home(storage):
    kitchen = storage.get("node-kitchen")
    lib = storage.get("node-lib")
    living = storage.get("node-living")
    north = storage.get("node-north")
    toilet = storage.get("node-toilet")

    layout = f"""
       Home data:\n
       +-------+------+----------+
       | 🌡{get_value(kitchen,'temp')}  | 🌡{get_value(lib,'temp')}  |  🌡{get_value(living, 'temp')}    |
       | %{get_value(kitchen, 'humi')}   | %{get_value(lib,'humi')}   |  %{get_value(living,'humi')}    |
       | LM  |   LM |   LM    |
       +-------+------+----------+
       | 🌡{get_value(toilet,'temp')}  |         | 🌡{get_value(north,'temp')}   |
       |  %{get_value(toilet,'humi')}  |         | %{get_value(north,'humi')}   |
       | LM  |          |   LM |
       +-------+---------+-------+
       """

    layout = layout.replace("L", get_value(kitchen, 'light')).replace("L", get_value(north,'light')).replace("L", get_value(living, 'light')).replace("L", get_value(toilet,'light')).replace("L", get_value(north,'light'))
    layout = layout.replace("M ", get_value(kitchen,'pir')).replace("M ", get_value(north,'pir')).replace("M ", get_value(living,'pir')).replace("M ", get_value(toilet,'pir')).replace("M ", get_value(north,'pir'))
    return layout


def room(room):
    pass
