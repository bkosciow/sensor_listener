from nextcloud_talk_bot_kosci.flask import init_server, app
from dotenv import load_dotenv
from node_listener.storage.storage import Storage
import logging
from node_listener.service.config import Config
import json
from node_bot.command import Command
import os

load_dotenv()

config = Config('config.ini')

Storage.set_engine(config.get_storage_engine())
storage = Storage()

def action(request):
    data = request.data.message.split()
    cmd = Command([
        '!sl <action>', '!sl <action> <module>'
    ])
    if cmd.parse(request.data.message):
        print(cmd.params)
        if cmd.command == '!sl':
            if cmd.action == "keys":
                data = storage.get_all()
                request.send_response( "\n".join(data.keys()), request.data['target']['id'])

            if cmd.action == "data":
                data = storage.get(cmd.module)
                request.send_response(json.dumps(data), request.data['target']['id'])


init_server(
    os.environ.get('NEXTCLOUD_URL'),
    os.environ.get('BOT_SECRET'),
    action
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('WEBHOOK_PORT'), debug=True)
