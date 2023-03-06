import requests


class Status:
    def __init__(self):
        self.message = None
        self.error = False
        self.initialized = False
        self.unrecoverable = False


class OctoprintApi:
    def __init__(self, name, url, token):
        self.name = name
        self.url = url
        self.token = token
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
        headers = {'X-Api-Key': self.token}
        return requests.get(self.url+uri, headers=headers)

    def post(self, uri, data):
        headers = {
            'X-Api-Key': self.token,
            'Content-Type': 'application/json',
        }
        return requests.post(self.url+uri, json=data, headers=headers)
