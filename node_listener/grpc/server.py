from node_listener.grpc.storage_pb2_grpc import *
from node_listener.grpc.provider import Provider
from concurrent import futures
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.server import SensorListener
from node_listener.service.config import Config


def serve(config_file, address="localhost:8765", max_workers=5):
    config = Config(config_file)

    Storage.set_engine(DictionaryEngine())
    storage = Storage()

    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()

    svr = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_ProviderServicer_to_server(Provider(storage), svr)
    svr.add_insecure_port(address)
    svr.start()
    svr.wait_for_termination()


if __name__ == "__main__":
    serve('../../config.ini')