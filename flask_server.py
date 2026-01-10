from nextcloud_talk_bot_kosci.flask import init_server, app
from dotenv import load_dotenv
from node_listener.storage.storage import Storage
from node_listener.service.config import Config
import json
import logging
import os
import time
from datetime import datetime

load_dotenv()

config = Config('config.ini')

Storage.set_engine(config.get_storage_engine())
storage = Storage()

patterns = [
    '!time',
    '!sl <action>', 
    '!sl <action> <module>',
    '!air',
    '!weather',
    '!home',
    '!home <room>'
]


def air_quality(data):
    result = {
        'PM25': None,
        'PM10': None,
        'CO': None,
        'O3': None,
    }
    icon = [
        '✅', '✅', '⚠️', '☠️', '☠️', '⚰️'
    ]
    max_value = 0
    for item in data:
        for key in data[item]:
            if key in result:
                if data[item][key] is not None and (result[key] is None or result[key] < data[item][key]):
                    result[key] = data[item][key]['index']
                    if data[item][key]['index'] > max_value:
                        max_value = data[item][key]['index']

    txt = icon[max_value] + " " + ("  |  ".join(f"__{k}__: {v}" for k, v in result.items()))

    return txt


def weather_current(data):
    return f" 🌡️{data['current']['temperature_current']}°C, 💦{data['current']['humidity']}%, {data['current']['pressure']} hPa pressure, 🌀{data['current']['wind_speed']} m/s 🧭{data['current']['wind_deg']}°, {data['current']['weather']}, ☁️{data['current']['clouds']}% "


def weather_forecast(data):
    text = ""
    for d in data['forecast']:
        weather = data['forecast'][d]
        text = text + " 📆 __" + d + "__ \n"
        text = text + f" 🌡️{weather['temperature_max']}/{weather['temperature_min']}°C | 💦{weather['humidity']}% | {weather['pressure']} hPa | "
        text = text + f" 🌀{weather['wind_speed']} m/s 🧭{weather['wind_deg']} | {weather['weather']} | ☁️{weather['clouds']}% "
        text = text + "\n"
    return text


def weather(data):
    return "__now__ :" + weather_current(data)+ "\n" + weather_forecast(data)


def format_temp(data):
    return f"{round(float(data))}"


def format_humi(data):
    return f"{round(float(data))}"


def home():
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


def action(request):
    cmd = request.parse_command(patterns)
    if cmd.result:
        if cmd.command == "!time":
            request.reply(" Executing...")
            time.sleep(10)
            request.post(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        print(cmd.params)
        if cmd.command == '!sl':
            if cmd.action == "keys":
                data = storage.get_all()
                request.reply("\n".join(data.keys()))

            if cmd.action == "data":
                data = storage.get(cmd.module)
                request.post(json.dumps(data))

        if cmd.command == "!air":
            request.post(air_quality(storage.get("openaq")))

        if cmd.command == "!weather":
            request.post(weather(storage.get('openweather')))

        if cmd.command == "!home":
            if cmd.room is not None:
                request.post(room(cmd.room))
            else:
                request.post(home())


init_server(
    os.environ.get('NEXTCLOUD_URL'),
    os.environ.get('BOT_SECRET'),
    action
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('WEBHOOK_PORT'), debug=True)
