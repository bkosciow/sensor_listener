import abc


class StorageEngineInterface(metaclass=abc.ABCMeta):
    def set(self, key, value):
        pass

    def get(self, key):
        pass

    def exists(self, key):
        pass