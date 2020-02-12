from .storage_pb2 import *
from .storage_pb2_grpc import *
import json


class Provider(ProviderServicer):
    def __init__(self, storage, queue):
        self.storage = storage
        self.queue = queue

    def get_storage(self, request, context):
        key = request.key
        if key == '':
            data = self.storage.get_all()
        else:
            data = self.storage.get(key)

        response = Response()
        response.data = json.dumps(data)

        return response

    def get_changes(self, request, context):
        while True:
            data = self.queue.get()
            response = Response()
            response.data = data
            yield response
