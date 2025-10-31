
import socket
import threading
import time


class NameServer:

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.server_socket = None
        self.names = {}
        self.lock = threading.Lock()
        self.stopped = threading.Event()

    def run(self, address_receiver=None, nameserver_address=None):
        if nameserver_address is None:
            nameserver_address = (
                '', 0) if self.restrict_to_localhost else ('', 9090)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(nameserver_address)

        if self.multicast_enabled:
            multicast_address = ('224.0.0.1', nameserver_address[1])
            self.server_socket.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            self.server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                          socket.inet_aton(multicast_address[0]) + socket.inet_aton('0.0.0.0'))

        threading.Thread(target=self._listen_for_requests).start()
        if address_receiver is not None:
            address_receiver(self.server_socket.getsockname())

    def stop(self):
        self.stopped.set()
        if self.server_socket is not None:
            self.server_socket.close()

    def _listen_for_requests(self):
        while not self.stopped.is_set():
            try:
                data, address = self.server_socket.recvfrom(1024)
                request = data.decode().split()
                if request[0] == 'register':
                    self._register(request[1], address)
                elif request[0] == 'lookup':
                    self._lookup(request[1], address)
                elif request[0] == 'unregister':
                    self._unregister(request[1])
            except socket.error:
                if not self.stopped.is_set():
                    raise

    def _register(self, name, address):
        with self.lock:
            self.names[name] = (address, time.time())
        self.server_socket.sendto(f'registered {name}'.encode(), address)

    def _lookup(self, name, address):
        with self.lock:
            if name in self.names:
                registered_address, _ = self.names[name]
                self.server_socket.sendto(
                    f'{registered_address[0]} {registered_address[1]}'.encode(), address)
            else:
                self.server_socket.sendto('not found'.encode(), address)

    def _unregister(self, name):
        with self.lock:
            if name in self.names:
                del self.names[name]
