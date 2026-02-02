from node_listener.service.config import Config
import node_listener.service.comm as comm
from node_listener.worker.openaq_worker import OpenaqWorker
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(message)s'
)
logging.getLogger('schedule').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


config = Config("config.ini")
comm.address = (config.get("general.ip"), int(config.get("general.port")))

p = json.loads(config.get('openaq.places'))

worker = OpenaqWorker({
    "apikey": config.get('openaq.apikey'),
    "user_agent": config.get('openaq.user_agent'),
    "places": p
})
sensors = worker.execute()

message = {
    'parameters': sensors,
    'event': "air.quality"
}
comm.send(message)
