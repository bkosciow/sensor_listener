from node_listener.grpc.storage_pb2_grpc import *
from node_listener.grpc.provider import Provider
from concurrent import futures
from node_listener.storage.storage import Storage
from node_listener.storage.dictionary_engine import DictionaryEngine
from node_listener.scheduler.task import Task
from node_listener.service.sensor_listener import SensorListener
from node_listener.service.config import Config
from node_listener.service.queue_bus import QueueBus
import queue


def serve(config_file):
    config = Config(config_file)

    Storage.set_engine(DictionaryEngine())
    storage = Storage()
    fifo = queue.Queue(maxsize=int(config["grpc"]["queue_size"]))
    queue_bus = QueueBus(fifo)
    storage.on('set', queue_bus.add_to_queue)

    Task.set_storage(storage)

    serverSensor = SensorListener(storage, config)
    serverSensor.start()

    svr = grpc.server(futures.ThreadPoolExecutor(max_workers=int(config["grpc"]["max_workers"])))
    add_ProviderServicer_to_server(Provider(storage, fifo), svr)
    svr.add_insecure_port(config["grpc"]["address"])
    svr.start()
    svr.wait_for_termination()


if __name__ == "__main__":
    serve('../../config.ini')