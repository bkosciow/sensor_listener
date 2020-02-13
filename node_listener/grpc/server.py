import queue
from node_listener.grpc.storage_pb2_grpc import *
from node_listener.grpc.provider import Provider
from concurrent import futures
from node_listener.service.queue_bus import QueueBus


class GRPCServer(object):
    def __init__(self, config, storage):
        self.storage = storage
        self.config = config
        self.fifo = queue.Queue(maxsize=int(self.config["grpc"]["queue_size"]))

    def start(self):
        queue_bus = QueueBus(self.fifo)
        self.storage.on('set', queue_bus.add_to_queue)
        svr = grpc.server(futures.ThreadPoolExecutor(max_workers=int(self.config["grpc"]["max_workers"])))
        add_ProviderServicer_to_server(Provider(self.storage, self.fifo), svr)
        svr.add_insecure_port(self.config["grpc"]["address"])
        svr.start()
        svr.wait_for_termination()
