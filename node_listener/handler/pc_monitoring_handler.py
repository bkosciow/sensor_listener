from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.hd44780_40_4 import Dump


class PCMonitoringHandler(HandlerInterface):
    def handle(self, message):
        any_data = False
        if message is not None and 'event' in message.data:
            if message['event'] == 'pc.monitoring':
                any_data = True
                self.call_on_all_workers(
                    message['node'],
                    {
                        'cpu_temperature': str(message['parameters']['cpu_temperature']),
                        'cpu_load': str(message['parameters']['cpu_load']),
                        'gpu_temperature': str(message['parameters']['gpu_temperature']),
                        'gpu_load': str(message['parameters']['gpu_load']),
                    }
                )
        if any_data:
            Dump.module_status({'name': 'PCMon', 'status': 2})

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}
