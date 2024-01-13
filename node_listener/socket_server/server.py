import errno
from threading import Thread
import socket
import json
from node_listener.service.hd44780_40_4 import Dump
import logging
logger = logging.getLogger(__name__)


class Job(Thread):
    def __init__(self, socket, storage):
        super().__init__()
        self.socket = socket
        self.storage = storage
        self.lock = False
        self.work = True

    def run(self):
        while self.work:
            try:
                data = self.socket.recv(1024)
                if data:
                    data = data.decode('utf8')
                    data = data.strip()
                    if not data:
                        self.stop()
                        break
                    if data == "quit":
                        self.stop()
                        break
                    if data == "get_all" or data == "getall":
                        self._handle_getall()
                else:
                    self.work = False
            except socket.error as e:
                if e.errno == 104:
                    logger.warning("Client disconnected")

            except IOError as  e:
                if e.errno == errno.EPIPE:
                    logger.warning("Client disconnected")
                else:
                    raise e

    def _handle_getall(self):
        for key in self.storage.get_all():
            data = {
                key: self.storage.get_all()[key],
            }
            self.send(json.dumps(data))

    def send(self, message):
        if not self.work:
            return False
        self.get_lock()
        self.socket.sendall((str(len(message)) + ":" + message.strip()).encode())
        self.release_lock()
        return True

    def get_lock(self):
        while self.lock:
            pass
        self.lock = True

    def release_lock(self):
        self.lock = False

    def stop(self):
        self.work = False
        self.socket.close()


class SocketServer(Thread):
    def __init__(self, config, storage):
        Thread.__init__(self)
        self.storage = storage
        self.config = config
        self.counter = 0
        self.working = False
        self.connections = []
        (addr, port) = self.config["socketserver"]["address"].split(":")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((addr, int(port)))
            self.socket.listen(int(self.config["socketserver"]["connections"]))
            self.working = True
        except OSError.errno as e:
            Dump.module_status({'name': 'ssock', "status": 5})
            raise e

    def run(self):
        self.storage.on('set', self.handle_new_data)
        Dump.module_status({'name': 'ssock', "status": 2})
        while self.working:
            client, address = self.socket.accept()
            logger.info('Connection from: ' + address[0] + ':' + str(address[1]))
            job = Job(client, self.storage)
            self.connections.append(job)
            job.start()

    def stop(self):
        self.working = False
        for t in self.connections:
            t.stop()
        self.socket.close()

    def send_all(self, message):
        for k, t in enumerate(self.connections):
            try:
                response = t.send(message)
                if not response:
                    t.stop()
                    self.connections[k] = None
            except IOError as e:
                if e.errno == errno.EPIPE or e.errno == errno.EBADMSG:
                    logger.warning("Client disconnected")
                    t.stop()
                    self.connections[k] = None
                else:
                    raise e

        self.connections = list(filter(None, self.connections))

    def handle_new_data(self, event):
        if bool(event.value):
            event.value['ts'] = self.counter
            self.counter += 1
            if self.counter == 60000:
                self.counter = 0
            data = {
                event.key: event.value,
            }
            self.send_all(json.dumps(data))
