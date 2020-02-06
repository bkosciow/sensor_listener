from pprint import pprint
from node_listener.worker.openweather_worker import OpenweatherWorker
from configparser import ConfigParser
import schedule
import time
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task

config = ConfigParser()
config.read("../../config.ini")

apikey = config["openweather"]["apikey"]
cities = {3103402: "Bielsko-Biała"}

w = OpenweatherWorker(cities, apikey)
# pprint(w.execute())

Storage.set_engine(DictionaryEngine())

storage = Storage()
Task.set_storage(storage)

bag = Task(w.execute, 'weather')


def dumpStorage():
    pprint(storage.get_all())


schedule.every(15).seconds.do(bag.execute)
schedule.every(6).seconds.do(dumpStorage)
while True:
    schedule.run_pending()
    time.sleep(1)
