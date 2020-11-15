from message_listener.server import Server
from node_listener.handler.node_one_handler import NodeOneHandler
from node_listener.handler.printer3d_handler import Printer3DHandler
from node_listener.scheduler.executor import Executor
from node_listener.scheduler.task import Task
from node_listener.worker.openweather_worker import OpenweatherWorker
from node_listener.worker.gios_worker import GiosWorker
from node_listener.worker.openaq_worker import OpenaqWorker
from pprint import pprint
import re


class SensorListener(object):
    def __init__(self, storage, config):
        self.storage = storage
        self.config = config

        self.svr = Server()
        self.executor = Executor()

        self._add_handlers()
        self._add_workers()
        #self.executor.every_seconds(5, DumpStorage(storage), True)

    def _add_handlers(self):
        if self.config.section_enabled("nodeone"):
            print("NodeOne enabled")
            self.svr.add_handler('NodeOne', NodeOneHandler(self.storage))

        if self.config.section_enabled("printer3d"):
            print("printer3d enabled")
            self.svr.add_handler('Printer3d', Printer3DHandler(self.storage))

    def _add_workers(self):
        if self.config.section_enabled("openweather"):
            w = OpenweatherWorker(self.config.get_dict("openweather.cities"), self.config["openweather"]["apikey"], self.config["general"]["user_agent"])
            self._start_task(w, 'openweather', self._parse_freq(self.config.get("openweather.freq")))

        if self.config.section_enabled("gios"):
            w = GiosWorker(self.config["gios"]["station_id"],  self.config["general"]["user_agent"])
            self._start_task(w, 'gios', self._parse_freq(self.config.get("gios.freq")))

        if self.config.section_enabled("openaq"):
            w = OpenaqWorker(self.config.get("openaq.city"),  self.config.get("openaq.location"),  self.config["general"]["user_agent"])
            self._start_task(w, 'openaq', self._parse_freq(self.config.get("openaq.freq")))

    def start(self):
        self.svr.start()
        self.executor.start()

    def _start_task(self, worker, name, freq):
        print("{} enabled".format(name))
        getattr(self.executor, "every_{}".format(freq['unit']))(freq['value'],  self._get_task(worker, name))

    def _get_task(self, worker, name):
        return Task(worker.execute, name)

    def _parse_freq(self, freq):
        raw_freq = re.findall(r'\d+|[a-zA-Z]', freq)
        freq = {
            'unit': None,
            'value': int(raw_freq[0])
        }

        if raw_freq[1] == "s" or raw_freq[1] == "seconds" or raw_freq[1] == "second":
            freq['unit'] = "seconds"
        elif raw_freq[1] == "m" or raw_freq[1] == "minutes" or raw_freq[1] == "minute":
            freq['unit'] = "minutes"
        elif raw_freq[1] == "h" or raw_freq[1] == "hours" or raw_freq[1] == "hour":
            freq['unit'] = "hours"

        return freq


class DumpStorage(object):
    def __init__(self, storage):
        self.storage = storage

    def execute(self):
        pprint(self.storage.get_all())
