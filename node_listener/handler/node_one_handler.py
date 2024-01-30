from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface


class NodeOneHandler(HandlerInterface, DebugInterface):
    def handle(self, message):
        any_data = False
        if message is not None and 'event' in message.data:
            if message['event'] == 'dht.status':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {
                        'temp': str(message['response']['temp']) if 'temp' in message['response'] else str(message['parameters']['temp']),
                        'humi': str(message['response']['humi']) if 'humi' in message['response'] else str(message['parameters']['humi']),
                    }
                )
            if message['event'] == 'detect.light':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {'light': True}
                )

            if message['event'] == 'detect.dark':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {'light': False}
                )
            if message['event'] == 'pir.movement':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {'pir': True}
                )

            if message['event'] == 'pir.nomovement':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {'pir': False}
                )

            if message['event'] == 'channels.response':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {'relay': message['response']}
                )

        if any_data:
            Dump.module_status({'name': 'Node1', 'status': 2})

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}

    def debug_name(self):
        return "Node1"
