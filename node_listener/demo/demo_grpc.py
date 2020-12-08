from node_listener.grpc.storage_pb2_grpc import *
from node_listener.grpc.storage_pb2 import *
from pprint import pprint
import json

# start server from grpc/server.py

# channel = grpc.insecure_channel('localhost:8765')
channel = grpc.insecure_channel('192.168.1.105:8765')
stub = ProviderStub(channel)
# key = Request(key='openaq')
key = Request(key=None)
response = stub.get_storage(key)
try:
    response = json.loads(response.data)
except ValueError as e:
    response = None

pprint(response)

# for response in stub.get_changes(EmptyRequest()):
#     print(response)

