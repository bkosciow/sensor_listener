from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.service.sensor_listener import SensorListener
from node_listener.service.config import Config
import node_listener.service.comm as comm
import time
from node_listener.service.hd44780_40_4 import Dump
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(message)s'
)
logging.getLogger('schedule').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def serve(config_file):
    config = Config(config_file)
    # Apprise
    if config.section_enabled('apprise'):
        from node_listener.service.apprise import ErrorHandler
        logging.getLogger().addHandler(ErrorHandler(config['apprise']))
        logger.info("Apprise enabled")

    # set broadcast socket
    comm.address = (config.get("general.ip"), int(config.get("general.port")))

    # Storage
    Storage.set_engine(DictionaryEngine())
    storage = Storage()
    Task.set_storage(storage)

    # Home Assistant integration
    ha = None
    if config.section_enabled('homeassistant'):
        logger.info("HomeAssistant enabled")
        from node_listener.homeassistant.homeassistant import HomeAssistant
        ha = HomeAssistant(config['homeassistant'])

    # starts a listener thread
    serverSensor = SensorListener(storage, config, ha)
    serverSensor.start()

    # starts local server for data
    socket_server = None
    if config.section_enabled("socketserver"):
        logger.info("SocketServer enabled")
        from node_listener.socket_server.server import SocketServer
        socket_server = SocketServer(config, storage)
        Dump.module_status({'name': 'ssock', "status": 1})
        socket_server.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        if config.section_enabled("socketserver"):
            if socket_server:
                socket_server.stop()
            logger.info("SocketServer stopped")


if __name__ == "__main__":
    logger.info("Starting app")
    serve('config.ini')
