from nextcloud_talk_bot_kosci.flask import init_server, app
from ollama_mcp_kun_kosci.aikun import AIKun
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
from nc_bot.assistant import query_assistant
import asyncio


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
    '!rem <prompt>'
]

assistant = AIKun(config.get('assistant.ollama_url'), config.get('assistant.ollama_model'))


def action(request):
    cmd = request.parse_command(patterns)
    print(cmd.result, cmd.command)
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

        if cmd.command == '!rem':
            print(cmd.text)
            response = query_assistant(config.get('assistant.url'), cmd.text)
            print(response)
            request.post(response['response']['content'])


async def main():
    await assistant.load_mcps(config.get_list('assistant.mcp_servers'))

asyncio.run(main())

init_server(
    config.get("ncbot.nc_url"),
    config.get('ncbot.secret'),
    action
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('WEBHOOK_PORT'), debug=True)
