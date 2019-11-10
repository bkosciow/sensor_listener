from . import StorageEngineInterface

GLUE = "."


class DictionaryEngine(StorageEngineInterface):
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        keys = key.split(GLUE)
        tmp = self.data
        for k in keys:
            if k == keys[-1]:
                tmp.update({k: value})
            else:
                tmp.update({k: {}})
                tmp = tmp[k]

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
