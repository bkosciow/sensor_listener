
def format_temp(data):
    return f"{round(float(data))}"


def format_humi(data):
    return f"{round(float(data))}"


def home(storage):
    kitchen = storage.get("node-kitchen")
    lib = storage.get("node-lib")
    living = storage.get("node-living")
    north = storage.get("node-north")
    toilet = storage.get("node-toilet")
    layout = f"""
    Home data:\n
    +-------+------+----------+
    | 🌡{format_temp(kitchen['temp'])}  | 🌡{format_temp(lib['temp'])}  |  🌡{format_temp(living['temp'])}    |
    | %{format_humi(kitchen['humi'])}   | %{format_humi(lib['humi'])}   |  %{format_humi(living['humi'])}    |
    | LM  |   LM |   LM    |
    +-------+------+----------+
    | 🌡{format_temp(toilet['temp'])}  |         | 🌡{format_temp(north['temp'])}   |
    |  %{format_humi(toilet['humi'])}  |         | %{format_humi(north['humi'])}   |
    | LM  |          |   LM |
    +-------+---------+-------+
    """

    layout = layout.replace("L", "💡" if kitchen['light'] else "  ", 1).replace("L", "💡" if north['light'] else "  ", 1).replace("L", "💡" if living['light'] else " ", 1).replace("L", "💡" if toilet['light'] else "  ", 1).replace("L", "💡" if north['light'] else "  ", 1)
    layout = layout.replace("M ", "🙋" if kitchen['pir'] else "  ", 1).replace("M ", "🙋" if north['pir'] else "  ", 1).replace("M ", "🙋" if living['pir'] else "  ", 1).replace("M ", "🙋" if toilet['pir'] else "  ", 1).replace("M ", "🙋" if north['pir'] else "  ", 1)
    return layout


def room(room):
    pass
