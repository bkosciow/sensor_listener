from message_listener.server import Server
from node_listener.handler.node_one_handler import NodeOneHandler
from node_listener.scheduler.executor import Executor
from node_listener.scheduler.task import Task
from node_listener.worker.openweather_worker import OpenweatherWorker
from pprint import pprint


class SensorListener(object):
    def __init__(self, storage, config):
        self.storage = storage
        self.config = config

        self.svr = Server()
        self.executor = Executor()

        self.svr.add_handler('NodeOne', NodeOneHandler(self.storage))

        w = OpenweatherWorker(
            self.config.get_dict("openweather.cities"), self.config["openweather"]["apikey"]
        )
        # self.executor.every_seconds(5, DumpStorage(storage), True)
        self.executor.every_seconds(15, Task(w.execute, 'weather'))

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