import abc


class Worker(metaclass=abc.ABCMeta):
    """Widget abstract"""
    @abc.abstractmethod
    def execute(self):
        """main body, called periodically"""
        pass

    def start(self):
        """called only once during add_handler"""
        pass

    def shutdown(self):
        """called only once during exiting"""
        pass
