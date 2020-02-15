from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.service.sensor_listener import SensorListener
from node_listener.service.config import Config
import time, os


def serve(config_file):
    config = Config(config_file)
    Storage.set_engine(DictionaryEngine())
    storage = Storage()
    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()

    if config.section_enabled("grpc"):
        print("gRPC server enabled")
        from node_listener.grpc.server import GRPCServer
        grpc_server = GRPCServer(config, storage)
        grpc_server.start()

    while True:
        time.sleep(2)


if __name__ == "__main__":
    print("Starting app")
    print(os.getcwd())
    serve('config.ini')
