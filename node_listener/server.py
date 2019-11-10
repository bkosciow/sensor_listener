from message_listener.server import Server
from node_listener.handler.node_one_handler import NodeOneHandler


class SensorListener(object):
    def __init__(self, storage):
        self.storage = storage

        self.svr = Server()
        self.svr.add_handler('NodeOne', NodeOneHandler(self.storage))

    def add_handler(self, name, handler, append_storage=True):
        pass

    def start(self):
        self.svr.start()

