from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.worker.octoprint_worker import OctoprintApi
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
                print(message)
                self._connect_to_octoprint(message.data)

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
        response = octoprint.post("/connection", {
            "command": "connect",
            "port": message['parameters']['port'],
            "baudrate": int(message['parameters']['baudrate']),
        })
        if response.status_code == 204:
            pass
        if response.status_code == 400:
            print(response.status_code)
            print(response.json())


