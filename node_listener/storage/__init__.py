import abc


class StorageEngineInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def exists(self, key):
        pass

    def close(self):
        pass
