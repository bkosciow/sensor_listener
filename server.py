from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.service.sensor_listener import SensorListener
from node_listener.service.config import Config
import time, os
from node_listener.service.hd44780_40_4 import Dump


def serve(config_file):
    config = Config(config_file)

    # Dump.module_status({'name': 'gRPC'})
    # Dump.module_status({'name': 'gRPC1'})
    # Dump.module_status({'name': 'gRPC2'})
    # Dump.module_status({'name': 'gRPC3'})
    # Dump.module_status({'name': 'gRPC4'})
    # Dump.module_status({'name': 'gRPC5'})
    # Dump.module_status({'name': 'gRPC64545'})
    #
    # return
    Storage.set_engine(DictionaryEngine())
    storage = Storage()
    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()

    if config.section_enabled("grpc"):
        print("gRPC server enabled")
        from node_listener.grpc.server import GRPCServer
        grpc_server = GRPCServer(config, storage)
        Dump.module_status({'name': 'gRPC', "status": 2})
        grpc_server.start()

    while True:
        time.sleep(2)


if __name__ == "__main__":
    print("Starting app")
    print(os.getcwd())
    serve('config.ini')
