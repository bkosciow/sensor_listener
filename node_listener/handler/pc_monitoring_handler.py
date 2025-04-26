from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
from node_listener.service.hd44780_40_4 import Dump
from node_listener.service.debug_interface import DebugInterface


class PCMonitoringHandler(HandlerInterface, DebugInterface):
    def handle(self, message):
        any_data = False
        if message is not None and 'event' in message.data:
            if message['event'] == 'pc.monitoring':
                any_data = True
                params = {
                        'cpu_temperature': message['parameters']['cpu_temperature'] if 'cpu_temperature' in message['parameters'] else 0,
                        'cpu_load': message['parameters']['cpu_load'] if 'cpu_load' in message['parameters'] else 0,
                        'gpu_temperature': message['parameters']['gpu_temperature'] if 'gpu_temperature' in message['parameters'] else 0,
                        'gpu_load': message['parameters']['gpu_load'] if 'gpu_load' in message['parameters'] else 0,
                    }
                for i in range(1, 8):
                    if 'hdd'+str(i)+'_temperature' in message['parameters']:
                        params['hdd'+str(i)+'_temperature'] = message['parameters']['hdd'+str(i)+'_temperature']

                self.call_on_all_workers(
                    message['node'],
                    params
                )
        if any_data:
            Dump.module_status({'name': self.debug_name(), 'status': 2})

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}

    def debug_name(self):
        return "PCmon"
