from nextcloud_talk_bot_kosci.fastapi import init_server, app
from ai_kun_kosci.aikun import AIKun
from dotenv import load_dotenv
from node_listener.storage.storage import Storage
from node_listener.service.config import Config
import json
import logging
import os
from nc_bot.air import air_quality
from nc_bot.weather import weather
from nc_bot.home import home, room
import openai
import httpx
from fastapi import HTTPException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

config = Config('config.ini')

Storage.set_engine(config.get_storage_engine())
storage = Storage()

patterns = [
    '!sl <action>',
    '!sl <action> <module>',
    '!air',
    '!weather',
    '!home',
    '!home <room>',
    '?rem <action>',
    '?rem <action> <object>',
    '!rem <prompt>',
    'Rem <prompt>'
]

assistant = AIKun(
    config.get('assistant.server_url'),
    config.get('assistant.apikey'),
    config.get('assistant.model')
)
initialized = False

async def action(request):
    global initialized
    try:
        if not initialized:
            await assistant.load_mcps(config.get_list('assistant.mcp_servers'))
            initialized = True

        cmd = request.parse_command(patterns)
        # print(cmd.result, cmd.command)
        if cmd.result:
            if cmd.command == '!sl':
                if cmd.action == "keys":
                    data = storage.get_all()
                    request.reply("\n".join(data.keys()))

                if cmd.action == "data":
                    data = storage.get(cmd.module)
                    request.post(json.dumps(data))

            if cmd.command == "!air":
                request.post(air_quality(storage.get("air-quality")))

            if cmd.command == "!weather":
                request.post(weather(storage.get('openweather')))

            if cmd.command == "!home":
                if cmd.room is not None:
                    request.post(room(cmd.room))
                else:
                    request.post(home(storage))
            if cmd.command == '?rem':
                if cmd.action == 'model' and cmd.object is None:
                    request.reply(assistant.model)
                elif cmd.action == 'model':
                    assistant.model = cmd.object
                    request.reply(f"model changed to {cmd.object}")

                if cmd.action == 'list':
                    if cmd.object == 'models':
                        models = await assistant.get_models()
                        text = "| name |\n"
                        text += "|------|\n"
                        for model in models:
                            text += f"| {model} |\n"
                        request.reply(text)

                if cmd.action == 'reload':
                    if cmd.object == 'mcp':
                        await assistant.clear_mcps()
                        await assistant.load_mcps(assistant.mcps)
                        request.reply("Tools reloaded")

            if cmd.command == '!rem' or cmd.command == 'Rem':
                request.react("🤖")
                response = await assistant.query(cmd.text)
                request.post(response.content)


    except (openai.NotFoundError, ConnectionError, httpx.HTTPStatusError) as e:
        logger.error(e)
        request.reply(str(e))

    except Exception as e:
        request.post(str(e))

init_server(
    config.get("ncbot.nc_url"),
    config.get('ncbot.secret'),
    action
)

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(
        "__main__:app", reload=True, host="0.0.0.0", port=int(os.environ.get('WEBHOOK_PORT', 8000)),
    )
