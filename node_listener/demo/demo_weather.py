from pprint import pprint
from node_listener.worker.openweather_worker import OpenweatherWorker

from configparser import ConfigParser

config = ConfigParser()
config.read("../../config.ini")

apikey = config["openweather"]["apikey"]
cities = {3103402: "Bielsko-Biała"}

w = OpenweatherWorker(cities, apikey)
pprint(w.execute())
