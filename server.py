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
    if config.section_enabled('nextcloud'):
        from node_listener.service.nextcloud import ErrorHandler
        logging.getLogger().addHandler(ErrorHandler(config))

    comm.address = (config.get("general.ip"), int(config.get("general.port")))
    Storage.set_engine(DictionaryEngine())
    storage = Storage()
    Task.set_storage(storage)
    ha = None
    if config.section_enabled('homeassistant'):
        logger.info("HomeAssistant enabled")
        from node_listener.homeassistant.homeassistant import HomeAssistant
        ha = HomeAssistant(config['homeassistant'])

    serverSensor = SensorListener(storage, config, ha)
    serverSensor.start()

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
            socket_server.stop()
            logger.info("SocketServer stopped")


if __name__ == "__main__":
    logger.info("Starting app")
    serve('config.ini')
