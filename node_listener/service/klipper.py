import requests


class Status:
    def __init__(self):
        self.message = None
        self.error = False
        self.initialized = False
        self.unrecoverable = False


class KlipperApi:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.status = Status()
        self.version = None
        self.connection = {
            'port': None,
            'baudrate': None
        }

    def clear_connection(self):
        self.connection = {
            'port': None,
            'baudrate': None
        }

    def get(self, uri):
        return requests.get(self.url + uri)

    def post(self, uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        return requests.post(self.url + uri, json=data, headers=headers)
