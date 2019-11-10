from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface


class SchedulerHandler(HandlerInterface):
    def __init__(self, *argv):
        super().__init__(argv)
        self.schedulers = []

    def handle(self, message):
        pass

    def add_scheduled_worker(self, worker, schedule):
        self.schedulers.append(worker)
