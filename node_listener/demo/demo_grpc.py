from node_listener.grpc.storage_pb2_grpc import *
from node_listener.grpc.storage_pb2 import *
import json

# start server from grpc/server.py

channel = grpc.insecure_channel('localhost:8765')
stub = ProviderStub(channel)
key = Request(key='openaq')
# key = Request(key=None)
response = stub.get_storage(key)
try:
    response = json.loads(response.data)
except ValueError as e:
    response = None

print(response)
