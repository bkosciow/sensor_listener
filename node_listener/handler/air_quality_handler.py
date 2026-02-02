from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface


class AirQuality(HandlerInterface, DebugInterface):
    def handle(self, message):
        any_data = False
        if message is not None and 'event' in message.data:
            if message['event'] == 'air.quality':
                any_data = True
                self.call_on_all_workers(
                    "air-quality",
                    message['parameters']
                )
        if any_data:
            Dump.module_status({'name': self.debug_name(), 'status': 2})

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}

    def debug_name(self):
        return "AirQ"
