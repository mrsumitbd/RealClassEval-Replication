
import threading
import time
import socket
import struct
import pickle
from typing import Optional, Tuple, Any


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._thread = None
        self._socket = None
        self._multicast_socket = None
        self._services = {}
        self._lock = threading.Lock()

    def run(self, address_receiver=None, nameserver_address=None):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._server_loop, args=(address_receiver, nameserver_address))
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        if not self._running:
            return

        self._running = False
        if self._socket:
            self._socket.close()
        if self._multicast_socket:
            self._multicast_socket.close()
        if self._thread:
            self._thread.join()

    def _server_loop(self, address_receiver, nameserver_address):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if nameserver_address:
            host, port = nameserver_address
        else:
            host = 'localhost' if self.restrict_to_localhost else ''
            port = 0  # Let OS choose a free port

        self._socket.bind((host, port))
        actual_port = self._socket.getsockname()[1]

        if address_receiver:
            address_receiver(
                (host if host else socket.gethostname(), actual_port))

        if self.multicast_enabled:
            self._setup_multicast()

        while self._running:
            try:
                data, addr = self._socket.recvfrom(4096)
                threading.Thread(target=self._handle_request,
                                 args=(data, addr)).start()
            except (socket.error, OSError):
                if self._running:
                    raise

    def _setup_multicast(self):
        self._multicast_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self._multicast_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        multicast_group = '224.1.1.1'
        multicast_port = 5007

        if not self.restrict_to_localhost:
            self._multicast_socket.bind(('', multicast_port))
            mreq = struct.pack('4sl', socket.inet_aton(
                multicast_group), socket.INADDR_ANY)
            self._multicast_socket.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        threading.Thread(target=self._multicast_loop, daemon=True).start()

    def _multicast_loop(self):
        while self._running:
            try:
                data, addr = self._multicast_socket.recvfrom(4096)
                threading.Thread(target=self._handle_multicast,
                                 args=(data, addr)).start()
            except (socket.error, OSError):
                if self._running:
                    raise

    def _handle_multicast(self, data, addr):
        try:
            request = pickle.loads(data)
            if request.get('type') == 'discover':
                response = {'type': 'response',
                            'address': self._socket.getsockname()}
                self._multicast_socket.sendto(pickle.dumps(response), addr)
        except (pickle.PickleError, AttributeError):
            pass

    def _handle_request(self, data, addr):
        try:
            request = pickle.loads(data)
            request_type = request.get('type')

            if request_type == 'register':
                with self._lock:
                    self._services[request['name']] = {
                        'address': request['address'],
                        'timestamp': time.time()
                    }
                response = {'status': 'ok'}
                self._socket.sendto(pickle.dumps(response), addr)

            elif request_type == 'lookup':
                with self._lock:
                    service = self._services.get(request['name'])
                    if service and (self.max_age is None or (time.time() - service['timestamp']) <= self.max_age):
                        response = {'status': 'ok',
                                    'address': service['address']}
                    else:
                        response = {'status': 'not_found'}
                self._socket.sendto(pickle.dumps(response), addr)

            elif request_type == 'unregister':
                with self._lock:
                    if request['name'] in self._services:
                        del self._services[request['name']]
                        response = {'status': 'ok'}
                    else:
                        response = {'status': 'not_found'}
                self._socket.sendto(pickle.dumps(response), addr)

        except (pickle.PickleError, AttributeError, KeyError):
            response = {'status': 'error'}
            self._socket.sendto(pickle.dumps(response), addr)
