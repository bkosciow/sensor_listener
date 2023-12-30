from . import StorageEngineInterface
from mergedeep import merge
from pprint import pprint

GLUE = "."


class DictionaryEngine(StorageEngineInterface):
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        try:
            keys = key.split(GLUE)
            tmp = self.data
            for k in keys:
                if k not in tmp:
                    tmp[k] = {}
                tmp = tmp[k]
            merge(tmp, value)
        except Exception as e:
            print(key)
            print(value)
            raise e

    def get(self, key):
        keys = key.split(GLUE)
        tmp = self.data
        for k in keys:
            if k in tmp:
                tmp = tmp[k]
            else:
                tmp = None
                break

        return tmp

    def exists(self, key):
        keys = key.split(GLUE)
        tmp = self.data
        for k in keys:
            if k in tmp:
                tmp = tmp[k]
            else:
                tmp = False
                break

        return True if tmp else False
