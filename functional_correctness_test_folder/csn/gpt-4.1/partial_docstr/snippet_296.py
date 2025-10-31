
import threading
import socket
import time


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._thread = None
        self._sock = None

    def _serve(self, address_receiver, nameserver_address):
        if self.restrict_to_localhost:
            bind_addr = '127.0.0.1'
        else:
            bind_addr = '0.0.0.0'
        if nameserver_address is None:
            nameserver_address = (bind_addr, 5353)
        else:
            if isinstance(nameserver_address, str):
                nameserver_address = (nameserver_address, 5353)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(nameserver_address)
        self._sock.settimeout(1.0)
        start_time = time.time()
        while self._running:
            try:
                data, addr = self._sock.recvfrom(1024)
                if address_receiver:
                    address_receiver(addr)
            except socket.timeout:
                pass
            if self.max_age is not None:
                if time.time() - start_time > self.max_age:
                    break
        self._sock.close()
        self._sock = None

    def run(self, address_receiver=None, nameserver_address=None):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._serve, args=(address_receiver, nameserver_address))
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join()
            self._thread = None
