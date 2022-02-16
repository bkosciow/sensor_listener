import json


class QueueBus(object):
    counter = 0

    def __init__(self, fifo):
        self.queue = fifo

    def add_to_queue(self, event):
        if bool(event.value):
            event.value['ts'] = self.counter
            self.counter += 1
            if self.counter == 60000:
                self.counter = 0
            data = {
                event.key: event.value,
            }
            if self.queue.full():
                self.queue.get()
            self.queue.put(json.dumps(data))

