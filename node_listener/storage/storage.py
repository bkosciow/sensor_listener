from .event import StorageEvent


class Storage(object):
    engine = None

    def __init__(self):
        self.events = {
            "set": [],
            "get": [],
        }

    def set_params(self, key, params):
        data = self.get(key, {})
        for p in params:
            data[p] = params[p]

        self.set(key, params)

    def exists(self, key):
        return self.engine.exists(key)

    def get(self, key, default=None):
        event = StorageEvent('set')

        if not self.engine.exists(key):
            value = default
        else:
            value = self.engine.get(key)

        event.key = key
        event.value = value
        self._dispatch_event('get', event)
        return value

    def set(self, key, value):
        self.engine.set(key, value)
        event = StorageEvent('set')
        event.key = key
        event.value = self.engine.get(key)
        self._dispatch_event('set', event)

    def get_all(self):
        return self.engine.data

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine

    def _dispatch_event(self, name, value):
        for event in self.events[name]:
            event(value)

    def on(self, name, event):
        if name not in self.events:
            raise ValueError("unsupported event "+name)

        self.events[name].append(event)

