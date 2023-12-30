from message_listener.server import Server
from node_listener.scheduler.executor import Executor
from node_listener.scheduler.task import Task
from pprint import pprint
import re
from node_listener.service.hd44780_40_4 import Dump
from importlib import import_module
from node_listener.service.debug_interface import DebugInterface
import logging
logger = logging.getLogger(__name__)


class SensorListener(object):
    def __init__(self, storage, config):
        self.storage = storage
        self.config = config
        self.svr = Server()
        self.executor = Executor()
        self._add_items()
        # self.executor.every_seconds(5, DumpStorage(storage), True)

    def _add_items(self):
        for section_name in self.config.sections():
            if self.config.section_enabled(section_name):
                handler_data = self.config.get_handler(section_name)
                if handler_data is not None:
                    handler_class = getattr(import_module(handler_data['module']), handler_data['class'])
                    handler_data['params'].insert(0, self.storage)
                    handler_instance = handler_class(*handler_data['params'])
                    print(handler_data['name'])
                    self.svr.add_handler(handler_data['name'], handler_instance)
                    if isinstance(handler_instance, DebugInterface):
                        Dump.module_status({'name': handler_instance.debug_name()})

                worker_data = self.config.get_worker(section_name)
                if worker_data:
                    worker_class = getattr(import_module(worker_data['module']), worker_data['class'])
                    worker_instance = worker_class(*worker_data['params'])
                    self._start_task(worker_instance, worker_data['name'], self._parse_freq(worker_data["freq"]))
                    if isinstance(worker_instance, DebugInterface):
                        Dump.module_status({'name': worker_instance.debug_name()})

    def start(self):
        self.svr.start()
        self.executor.start()

    def _start_task(self, worker, name, freq):
        logger.info("{} enabled".format(name))
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
        print(a["ender5pro"].keys())
