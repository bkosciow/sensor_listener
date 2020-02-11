from message_listener.server import Server
from node_listener.handler.node_one_handler import NodeOneHandler
from node_listener.scheduler.executor import Executor
from node_listener.scheduler.task import Task
from node_listener.worker.openweather_worker import OpenweatherWorker
from node_listener.worker.gios_worker import GiosWorker
from node_listener.worker.openaq_worker import OpenaqWorker
from pprint import pprint


class SensorListener(object):
    def __init__(self, storage, config):
        self.storage = storage
        self.config = config

        self.svr = Server()
        self.executor = Executor()

        if self.config.section_enabled("nodeone"):
            print("NodeOne enabled")
            self.svr.add_handler('NodeOne', NodeOneHandler(self.storage))

        if self.config.section_enabled("openweather"):
            print("Openweather enabled")
            w = OpenweatherWorker(
                self.config.get_dict("openweather.cities"), self.config["openweather"]["apikey"], self.config["general"]["user_agent"]
            )
            self.executor.every_seconds(15, Task(w.execute, 'weather'))

        if self.config.section_enabled("gios"):
            print("GIOS enabled")
            g = GiosWorker(self.config["gios"]["station_id"],  self.config["general"]["user_agent"])
            self.executor.every_minutes(30, Task(g.execute, 'gios'))

        if self.config.section_enabled("openaq"):
            print("OpenAQ enabled")
            aq = OpenaqWorker(self.config.get("openaq.city"),  self.config.get("openaq.location"),  self.config["general"]["user_agent"])
            self.executor.every_minutes(30, Task(aq.execute, 'openaq'))

        # self.executor.every_seconds(5, DumpStorage(storage), True)

    def add_handler(self, name, handler, append_storage=True):
        pass

    def start(self):
        self.svr.start()
        self.executor.start()


class DumpStorage(object):
    def __init__(self, storage):
        self.storage = storage

    def execute(self):
        pprint(self.storage.get_all())


# class serve(object):
#     def __init__(self):


