from pprint import pprint
from node_listener.worker.openaq_worker import OpenaqWorker
from node_listener.service.config import Config

config = Config('../../config.ini')

w = OpenaqWorker(
    config["openaq"]["city"],
    config["openaq"]["location"],
    config["general"]["user_agent"]
)
pprint(w.execute())
