
import socket
import threading
import time
from collections import defaultdict


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.running = False
        self.server_socket = None
        self.thread = None
        self.names = defaultdict(dict)
        self.lock = threading.Lock()

    def run(self, address_receiver=None, nameserver_address=None):
        '''Run the listener and answer to requests.'''
        if self.running:
            return

        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if nameserver_address:
            self.server_socket.bind(nameserver_address)
        else:
            if self.restrict_to_localhost:
                self.server_socket.bind(('127.0.0.1', 0))
            else:
                self.server_socket.bind(('', 0))

        self.thread = threading.Thread(target=self._listen)
        self.thread.start()

    def _listen(self):
        while self.running:
            data, addr = self.server_socket.recvfrom(1024)
            self._handle_request(data, addr)

    def _handle_request(self, data, addr):
        parts = data.decode().split()
        if not parts:
            return

        command = parts[0].lower()
        if command == 'register':
            if len(parts) < 3:
                return
            name = parts[1]
            address = parts[2]
            with self.lock:
                self.names[name][addr] = time.time()
        elif command == 'lookup':
            if len(parts) < 2:
                return
            name = parts[1]
            with self.lock:
                addresses = list(self.names.get(name, {}).keys())
            response = ' '.join(addresses).encode()
            self.server_socket.sendto(response, addr)

    def stop(self):
        '''Stop the nameserver.'''
        if not self.running:
            return

        self.running = False
        self.server_socket.close()
        self.thread.join()
