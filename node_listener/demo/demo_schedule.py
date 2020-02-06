from pprint import pprint
from node_listener.worker.openweather_worker import OpenweatherWorker
from configparser import ConfigParser
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.scheduler.executor import Executor


class DumpStorage(object):
    def __init__(self, storage):
        self.storage = storage

    def execute(self):
        pprint(self.storage.get_all())


Storage.set_engine(DictionaryEngine())
storage = Storage()

Task.set_storage(storage)

config = ConfigParser()
config.read("../../config.ini")

apikey = config["openweather"]["apikey"]
cities = {3103402: "Bielsko-Biała"}

w = OpenweatherWorker(cities, apikey)

executor = Executor()
executor.every_seconds(15, Task(w.execute, 'weather'))
executor.every_seconds(5, DumpStorage(storage), True)

executor.start()
