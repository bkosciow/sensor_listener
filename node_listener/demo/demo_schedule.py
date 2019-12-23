from pprint import pprint
from node_listener.worker.openweather_worker import OpenweatherWorker
from configparser import ConfigParser
import schedule
import time

config = ConfigParser()
config.read("../../config.ini")

apikey = config["openweather"]["apikey"]
cities = {3103402: "Bielsko-Biała"}

w = OpenweatherWorker(cities, apikey)
# pprint(w.execute())

class Bag(object):
    def __init__(self, func):
        self.func = func

    def execute(self):
        pprint(self.func())


bag = Bag(w.execute)

schedule.every(15).seconds.do(bag.execute)

while True:
    schedule.run_pending()
    time.sleep(1)
