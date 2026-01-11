from nextcloud_talk_bot_kosci.flask import init_server, app
from dotenv import load_dotenv
from node_listener.storage.storage import Storage
from node_listener.service.config import Config
import json
import logging
import os
import time
from datetime import datetime
from nc_bot.air import air_quality
from nc_bot.weather import weather
from nc_bot.home import home, room

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


def action(request):
    cmd = request.parse_command(patterns)
    if cmd.result:
        if cmd.command == "!time":
            request.reply(" Executing...")
            time.sleep(10)
            request.post(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # print(cmd.params)
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
                request.post(home(storage))


init_server(
    os.environ.get('NEXTCLOUD_URL'),
    os.environ.get('BOT_SECRET'),
    action
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('WEBHOOK_PORT'), debug=True)
