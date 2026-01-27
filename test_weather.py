from node_listener.service.config import Config
from node_listener.worker.openweather_worker import OpenweatherWorker

import json
from pprint import pprint

config = Config('config.ini')
p = json.loads(config.get('openweather.worker_parameters'))[0]
worker = OpenweatherWorker(p)

pprint(worker.execute())
