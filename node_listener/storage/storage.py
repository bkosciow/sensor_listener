

class Storage(object):
    engine = None
    # last_key = 'last_data'

    def set_params(self, key, params):
        data = self.get(key, {})
        for p in params:
            data[p] = params[p]

        self.set(key, data)

    # def get_sensor_response(self, node_name, key):
    #     if not self.engine.exists(node_name):
    #         return Response(i18n.t("main.room.not_known"), 400)
    #
    #     data = self.engine.get(node_name)
    #     if key in data:
    #         return Response(data[key])
    #     else:
    #         return Response(i18n.t("main.room.no_data"), 400)

    # def get_last_value(self, key, default=None):
    #     data = self.get(self.last_key, {})
    #
    #     if key in data:
    #         return data[key]
    #
    #     return default

    # def set_last_value(self, key, value):
    #     data = self.get(self.last_key, {})
    #     data[key] = value
    #     self.engine.set(self.last_key, data)

    def exists(self, key):
        return self.engine.exists(key)

    def get(self, key, default=None):
        if not self.engine.exists(key):
            return default

        return self.engine.get(key)

    def set(self, key, value):
        self.engine.set(key, value)

    def get_all(self):
        return self.engine.data

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine
