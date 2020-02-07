from pprint import pprint
from node_listener.worker.gios_worker import GiosWorker

from configparser import ConfigParser

config = ConfigParser()
config.read("../../config.ini")

station_id = config["gios"]["station_id"]

w = GiosWorker(station_id)
pprint(w.execute())
