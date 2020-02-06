

class Task(object):
    storage = None

    def __init__(self, func, storage_key):
        self.func = func
        self.storage_key = storage_key

    def execute(self):
        result = self.func()
        self.storage.set(self.storage_key, result)

    @classmethod
    def set_storage(cls, storage):
        cls.storage = storage
