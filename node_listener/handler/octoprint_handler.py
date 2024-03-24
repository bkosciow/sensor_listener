import errno

import requests.exceptions
from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.octoprint import OctoprintApi
import threading
import time


class OctoprintHandler(HandlerInterface):
    def __init__(self, dictionary, config):
        if type(config) is not dict:
            raise ValueError("config must be a dict")
        super().__init__(dictionary)
        self.printer = None
        self._debug_name = config["debug_name"]
        self.printer = OctoprintApi(config["node_name"], config["url"], config["key"])

    def handle(self, message):
        if message is not None and 'event' in message.data:
            try:
                if message.data['event'] == "octoprint.connect" and 'parameters' in message.data:
                    self._connect_to_octoprint(message.data)
                if message.data['event'] == "octoprint.get_filelist" and 'parameters' in message.data:
                    self._get_filelist(message.data)
                if message.data['event'] == "octoprint.print_start" and 'parameters' in message.data:
                    self._start_print(message.data)
                if message.data['event'] == "octoprint.print_stop" and 'parameters' in message.data:
                    self._stop_print(message.data)
                if message.data['event'] == "octoprint.print_pause" and 'parameters' in message.data:
                    self._pause_print(message.data)
                if message.data['event'] == "octoprint.print_resume" and 'parameters' in message.data:
                    self._resume_print(message.data)
            except IOError as e:
                if e.errno == errno.EIDRM:
                    pass
            except requests.exceptions.ConnectionError:
                pass

    def _connect_to_octoprint(self, message):
        if 'port' not in message['parameters']:
            return False
        if 'baudrate' not in message['parameters']:
            return False
        if 'node_name' not in message['parameters']:
            return False
        t = threading.Thread(target=self._call_connect, args=(self.printer, message), daemon=True)
        t.start()

    def _disconnect_from_octoprint(self):
        pass

    def _call_disconnect(self, octoprint):
        octoprint.post("/connection", {
            "command": "disconnect",
        })

    def _call_connect(self, octoprint, message):
        response = octoprint.post("/connection", {
            "command": "connect",
            "port": message['parameters']['port'],
            "baudrate": int(message['parameters']['baudrate']),
        })
        if response.status_code != 204:
            return

        time.sleep(3)
        fuse = 3
        while fuse:
            response = octoprint.get('/connection')
            response_json = response.json()
            if response_json['current']['state'] == "Operational":
                return
            fuse -= 1
            time.sleep(3)

        self._call_disconnect(octoprint)

    def _get_filelist(self, message):
        if 'node_name' not in message['parameters']:
            return False
        response = self.printer.get("/files?recursive=true")
        response_json = response.json()
        files = []
        for item in response_json['files']:
            if item['origin'] == "local":
                if "folder" in item['typePath']:
                    for subitems in item['children']:
                        files.append({"display": subitems['display'], "path": subitems['path']})
                else:
                    files.append({"display": item['display'], "path": item['path']})
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
        path = message['parameters']['path']
        self.printer.post('/files/local/'+path, {'command': "select", "print": True})

    def _stop_print(self, message):
        self.printer.post("/job", {"command": "cancel"})

    def _pause_print(self, message):
        self.printer.post("/job", {"command": "pause", "action": "pause"})

    def _resume_print(self, message):
        self.printer.post("/job", {"command": "pause", "action": "resume"})

    def call_on_all_workers(self, node_name, params):
        {w.set(node_name, params) for w in self.workers}
