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
                        'cpu_temperature': message['parameters']['cpu_temperature'] if 'cpu_temperature' in message['parameters'] else 0,
                        'cpu_load': message['parameters']['cpu_load'] if 'cpu_load' in message['parameters'] else 0,
                        'gpu_temperature': message['parameters']['gpu_temperature'] if 'gpu_temperature' in message['parameters'] else 0,
                        'gpu_load': message['parameters']['gpu_load'] if 'gpu_load' in message['parameters'] else 0,
                    }
                )
        if any_data:
            Dump.module_status({'name': 'PCMon', 'status': 2})

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}
