from .storage_pb2 import *
from .storage_pb2_grpc import *
import json


class Provider(ProviderServicer):
    def __init__(self, storage):
        self.storage = storage

    def get_storage(self, request, context):
        key = request.key
        if key == '':
            data = self.storage.get_all()
        else:
            data = self.storage.get(key)
        print("got", key)

        response = Response()
        response.data = json.dumps(data)

        return response
