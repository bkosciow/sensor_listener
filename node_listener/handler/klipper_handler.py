from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.klipper import KlipperApi
from node_listener.service.hd44780_40_4 import Dump
import time


class KlipperHandler(HandlerInterface):
    def __init__(self, dictionary, config):
        if type(config) is not dict:
            raise ValueError("config must be a dict")
        super().__init__(dictionary)
        self.printer = None
        self._debug_name = config["debug_name"]
        self.printer = KlipperApi(config["node_name"], config["url"])

    def handle(self, message):
        if message is not None and 'event' in message.data:
            if message.data['event'] == "klipper.get_filelist" and 'parameters' in message.data:
                self._get_filelist(message.data)
            if message.data['event'] == "klipper.print_start" and 'parameters' in message.data:
                self._start_print(message.data)
            if message.data['event'] == "klipper.print_stop" and 'parameters' in message.data:
                self._stop_print(message.data)
            if message.data['event'] == "klipper.print_pause" and 'parameters' in message.data:
                self._pause_print(message.data)
            if message.data['event'] == "klipper.print_resume" and 'parameters' in message.data:
                self._resume_print(message.data)

    def _get_filelist(self, message):
        response = self.printer.get('/server/files/list')
        response_json = response.json()
        files = []
        for item in response_json['result']:
            files.append({"display": item['path'], "path": item['path']})

        self.call_on_all_workers(
            self.printer.name,
            {'files': {
                "list": files,
                "ts":  time.time()
            }}
        )

    def _start_print(self, message):
        if 'path' not in message['parameters']:
            return False
        self.printer.post('/printer/print/start?filename='+message['parameters']['path'], [])

    def _stop_print(self, message):
        self.printer.post('/printer/print/cancel', [])

    def _pause_print(self, message):
        self.printer.post('/printer/print/pause', [])

    def _resume_print(self, message):
        self.printer.post('/printer/print/resume', [])

    def call_on_all_workers(self, node_name, params):
        {w.set(node_name, params) for w in self.workers}
