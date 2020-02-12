import json


class QueueBus(object):
    def __init__(self, fifo):
        self.queue = fifo

    def add_to_queue(self, event):
        if bool(event.value):
            data = {
                event.key: event.value
            }
            if self.queue.full():
                self.queue.get()
            self.queue.put(json.dumps(data))