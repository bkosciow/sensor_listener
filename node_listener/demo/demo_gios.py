from pprint import pprint
from node_listener.worker.gios_worker import GiosWorker
from node_listener.service.config import Config

config = Config('../../config.ini')

station_id = config["gios"]["station_id"]

w = GiosWorker(station_id,  config["general"]["user_agent"])
pprint(w.execute())
