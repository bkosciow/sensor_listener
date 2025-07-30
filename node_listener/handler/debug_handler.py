from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface


class DebugHandler(HandlerInterface):
    def handle(self, message):
        if message is not None and 'event' in message.data:
            if message['event'] == 'lcd.content':
                pass
                # print(message)
