from message_listener.server import Server
# from node_listener.handler.printer3d_handler import Printer3DHandler
from node_listener.scheduler.executor import Executor
from node_listener.scheduler.task import Task
from node_listener.worker.openweather_worker import OpenweatherWorker
from node_listener.worker.gios_worker import GiosWorker
from node_listener.worker.openaq_worker import OpenaqWorker
from node_listener.worker.octoprint_worker import OctoprintWorker
from node_listener.worker.klipper_worker import KlipperWorker
from pprint import pprint
import re
from node_listener.service.hd44780_40_4 import Dump
from importlib import import_module
from node_listener.service.debug_interface import DebugInterface


class SensorListener(object):
    def __init__(self, storage, config):
        self.storage = storage
        self.config = config

        self.svr = Server()
        self.executor = Executor()

        # self._add_handlers()
        self._add_workers()
        self._add_items()
        # self.executor.every_seconds(5, DumpStorage(storage), True)

    def _add_items(self):
        for section_name in self.config.sections():
            if self.config.section_enabled(section_name):
                handlerData = self.config.get_handler(section_name)
                if handlerData is not None:
                    print(handlerData)
                    handlerClass = getattr(import_module(handlerData['module']), handlerData['class'])
                    handlerData['params'].insert(0, self.storage)
                    handlerInstance = handlerClass(*handlerData['params'])
                    self.svr.add_handler(handlerData['name'], handlerInstance)
                    if isinstance(handlerInstance, DebugInterface):
                        Dump.module_status({'name': handlerInstance.debug_name()})

            # params = []
            # config_params = self.config.get(section_name + ".handler")
            # handlerInstance

            # if self.config.get(section_name + ".worker"):
            #     print("worker")

            # print("Section %s skipped" %(section_name))

    def _add_workers(self):
        if self.config.section_enabled("openweather"):
            w = OpenweatherWorker(self.config.get_dict("openweather.cities"), self.config["openweather"]["apikey"], self.config["general"]["user_agent"])
            self._start_task(w, 'openweather', self._parse_freq(self.config.get("openweather.freq")))
            Dump.module_status({'name': 'OpenW'})

        if self.config.section_enabled("gios"):
            w = GiosWorker(self.config["gios"]["station_id"],  self.config["general"]["user_agent"])
            self._start_task(w, 'gios', self._parse_freq(self.config.get("gios.freq")))
            Dump.module_status({'name': 'gios'})

        if self.config.section_enabled("openaq"):
            w = OpenaqWorker(self.config.get("openaq.city"),  self.config.get("openaq.location"),  self.config["general"]["user_agent"])
            self._start_task(w, 'openaq', self._parse_freq(self.config.get("openaq.freq")))
            Dump.module_status({'name': 'opnAQ'})

        if self.config.section_enabled("octoprint"):
            w = OctoprintWorker(self.config.get_dict('octoprint.printers'))
            self._start_task(w, '3dprinters', self._parse_freq(self.config.get("octoprint.freq")))
            Dump.module_status({'name': 'Octo'})

        if self.config.section_enabled("klipper"):
            w = KlipperWorker(self.config.get_dict('klipper.printers'))
            self._start_task(w, '3dprinters', self._parse_freq(self.config.get("klipper.freq")))
            Dump.module_status({'name': 'Klipp'})

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
        a = self.storage.get_all()
        print(a)
        # if "octoprint" in a:
        #     pprint(a['octoprint'])
