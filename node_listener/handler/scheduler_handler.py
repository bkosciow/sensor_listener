from message_listener.abstract.handler_interface import \
    Handler as HandlerInterface
import schedule


class SchedulerHandler(HandlerInterface):
    def __init__(self, *argv):
        super().__init__(argv)
        self.schedulers = []

    def handle(self, message):
        pass

    def add_scheduled_worker(self, worker, every, occurence, at):
        worker.start()
        self.schedulers.append(worker)
        schedule.every()
