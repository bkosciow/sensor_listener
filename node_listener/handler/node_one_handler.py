from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface


class NodeOneHandler(HandlerInterface):
    def handle(self, message):
        if message is not None and 'event' in message.data:
            if message['event'] == 'dht.status':
                self.call_on_all_workers(
                    message['node'],
                    {
                        'temp': str(message['response']['temp']),
                        'humi': str(message['response']['humi'])
                    }
                )
            if message['event'] == 'detect.light':
                self.call_on_all_workers(
                    message['node'],
                    {'light': True}
                )

            if message['event'] == 'detect.dark':
                self.call_on_all_workers(
                    message['node'],
                    {'light': False}
                )
            if message['event'] == 'pir.movement':
                self.call_on_all_workers(
                    message['node'],
                    {'pir': True}
                )

            if message['event'] == 'pir.nomovement':
                self.call_on_all_workers(
                    message['node'],
                    {'pir': False}
                )

            if message['event'] == 'channels.response':
                self.call_on_all_workers(
                    message['node'],
                    {'relay': message['response']}
                )

    def call_on_all_workers(self, node_name, params):
        {w.set_params(node_name, params) for w in self.workers}