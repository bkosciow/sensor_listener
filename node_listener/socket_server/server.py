from threading import Thread
import socket
import json


class Job(Thread):
    def __init__(self, socket, storage):
        super().__init__()
        self.socket = socket
        self.storage = storage
        self.lock = False
        self.work = True

    def run(self):
        while self.work:
            data = self.socket.recv(1024).decode('utf8')
            data = data.strip()
            reply = 'OK...' + data
            print("|"+data+"|")

            if not data:
                break

            if data == "quit":
                break
            if data == "get_all" or data == "getall":
                self._handle_getall()

            self.socket.sendall(reply.encode())

        self.socket.close()
        self.work = False

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
        self.socket.sendall(message.encode())
        self.release_lock()
        return True

    def get_lock(self):
        while self.lock:
            pass
        self.lock = True

    def release_lock(self):
        self.lock = False


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
            print("BUM")
            raise e

    def run(self):
        self.storage.on('set', self.handle_new_data)

        while self.working:
            client, address = self.socket.accept()
            print('Connection from: ' + address[0] + ':' + str(address[1]))
            job = Job(client, self.storage)
            self.connections.append(job)
            job.start()

    def stop(self):
        self.working = False
        self.socket.close()
        for t in self.connections:
            t.stop()

    def send_all(self, message):
        for t in self.connections:
            response = t.send(message)
            # if not response:

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
