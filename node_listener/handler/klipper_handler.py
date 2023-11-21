from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.klipper import KlipperApi
import time


class KlipperHandler(HandlerInterface):
    def __init__(self, dictionary, configs):
        if type(configs) is not dict:
            raise ValueError("klippers must be a dict")
        super().__init__(dictionary)
        self.printers = {}
        for name in configs:
            klipper = KlipperApi(name, configs[name][0])
            self.printers[name] = klipper

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

    def _get_klipper(self, message):
        if 'node_name' not in message['parameters']:
            return None
        node_name = message['parameters']['node_name']
        if node_name not in self.printers:
            return None
        return self.printers[node_name]

    def _get_filelist(self, message):
        klipper = self._get_klipper(message)
        response = klipper.get('/server/files/list')
        response_json = response.json()
        files = []
        for item in response_json['result']:
            files.append({"display": item['path'], "path": item['path']})

        self.call_on_all_workers(
            "3dprinters",
            {message['parameters']['node_name']: {'files': {
                "list": files,
                "ts":  time.time()
            }}}
        )

    def _start_print(self, message):
        if 'path' not in message['parameters']:
            return False
        klipper = self._get_klipper(message)
        klipper.post('/printer/print/start?filename='+message['parameters']['path'], [])

    def _stop_print(self, message):
        klipper = self._get_klipper(message)
        klipper.post('/printer/print/cancel', [])

    def _pause_print(self, message):
        klipper = self._get_klipper(message)
        klipper.post('/printer/print/pause', [])

    def _resume_print(self, message):
        klipper = self._get_klipper(message)
        klipper.post('/printer/print/resume', [])

    def call_on_all_workers(self, node_name, params):
        {w.set(node_name, params) for w in self.workers}