from node_listener.service.config import Config
from node_listener.worker.gios_worker import GiosWorker
from node_listener.worker.openaq_worker import OpenaqWorker
import json
from pprint import pprint

config = Config('config.ini')
p = json.loads(config.get('gios.worker_parameters'))[0]
worker = GiosWorker(p)
print(worker.execute())

p = json.loads(config.get('openaq.worker_parameters'))[0]
worker = OpenaqWorker(p)
print(worker.execute())
