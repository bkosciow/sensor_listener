from pprint import pprint
from node_listener.worker.openweather_worker import OpenweatherWorker
from node_listener.service.config import Config

config = Config('../../config.ini')

apikey = config["openweather"]["apikey"]
cities = {3103402: "Bielsko-Biała"}

w = OpenweatherWorker(cities, apikey, config["general"]["user_agent"])
pprint(w.execute())
