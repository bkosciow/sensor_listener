from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.octoprint import OctoprintApi
import threading
import time
from node_listener.service.hd44780_40_4 import Dump


class OctoprintHandler(HandlerInterface):
    def __init__(self, dictionary, octoprints):
        if type(octoprints) is not dict:
            raise ValueError("octoprints must be a dict")
        super().__init__(dictionary)
        self.octoprints = {}
        for name in octoprints:
            octoprint = OctoprintApi(name, octoprints[name][1], octoprints[name][0])
            self.octoprints[name] = octoprint

    def handle(self, message):
        if message is not None and 'event' in message.data:
            if message.data['event'] == "octoprint.connect" and 'parameters' in message.data:
                # print(message)
                self._connect_to_octoprint(message.data)
            if message.data['event'] == "octoprint.get_filelist" and 'parameters' in message.data:
                self._get_filelist(message.data)

    def _connect_to_octoprint(self, message):
        if 'port' not in message['parameters']:
            return False
        if 'baudrate' not in message['parameters']:
            return False
        if 'node_name' not in message['parameters']:
            return False
        node_name = message['parameters']['node_name']
        if node_name not in self.octoprints:
            return False
        octoprint = self.octoprints[node_name]
        t = threading.Thread(target=self._call_connect, args=(octoprint, message), daemon=True)
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
        node_name = message['parameters']['node_name']
        if node_name not in self.octoprints:
            return False
        octoprint = self.octoprints[node_name]
        response = octoprint.get("/files?recursive=true")
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
            "octoprint."+node_name,
            {'files': {
                "list": files,
                "ts":  time.time()
            }}
        )

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}
