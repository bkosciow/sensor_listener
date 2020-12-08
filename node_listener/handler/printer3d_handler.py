from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface


class Printer3DHandler(HandlerInterface):
    def handle(self, message):
        if message is not None and 'event' in message.data:
            if message['event'] == "3dprinter.status":
                self.call_on_all_workers(
                    message['node'],
                    {
                        'status': message['parameters']['status']
                    }
                )
                if message['parameters']['status'] in ['connected', 'disconnected']:
                    self.call_on_all_workers(
                        message['node'],
                        {
                            'percentage': "0",
                            'eta': "0",
                            'secondsLeft': "0",
                            'printTimeLeft': "0",
                            'totalLayers': "0",
                            'currentLayer': "0",
                        }
                    )
            if message['event'] == '3dprinter.progress':
                self.call_on_all_workers(
                    message['node'],
                    {
                        'percentage': message['parameters']['percentage'],
                        'eta': message['parameters']['estimatedEndTime'],
                        'secondsLeft': message['parameters']['printTimeLeftInSeconds'],
                        'printTimeLeft':  message['parameters']['printTimeLeft'],
                        'totalLayers':  message['parameters']['totalLayers'],
                        'currentLayer':  message['parameters']['currentLayer'],
                    }
                )

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}