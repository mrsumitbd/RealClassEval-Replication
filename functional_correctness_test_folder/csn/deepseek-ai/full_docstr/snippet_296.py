
import socket
import threading
import time
import pickle
from typing import Optional, Tuple, Any


class NameServer:
    '''The name server.'''

    def __init__(self, max_age: Optional[float] = None, multicast_enabled: bool = True, restrict_to_localhost: bool = False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._socket = None
        self._thread = None
        self._registry = {}
        self._lock = threading.Lock()

    def run(self, address_receiver: Optional[Any] = None, nameserver_address: Optional[Tuple[str, int]] = None):
        '''Run the listener and answer to requests.'''
        if self._running:
            return

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if nameserver_address is None:
            host = '127.0.0.1' if self.restrict_to_localhost else ''
            port = 0  # Let OS choose a free port
        else:
            host, port = nameserver_address

        self._socket.bind((host, port))
        _, actual_port = self._socket.getsockname()

        if address_receiver is not None:
            address_receiver((host, actual_port))

        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def _listen(self):
        '''Listen for incoming requests and respond.'''
        while self._running:
            try:
                data, addr = self._socket.recvfrom(4096)
                threading.Thread(target=self._handle_request,
                                 args=(data, addr)).start()
            except OSError:
                if not self._running:
                    break
                raise

    def _handle_request(self, data: bytes, addr: Tuple[str, int]):
        '''Handle a single request.'''
        try:
            request = pickle.loads(data)
            if request.get('type') == 'register':
                with self._lock:
                    self._registry[request['name']] = {
                        'address': request['address'],
                        'timestamp': time.time()
                    }
                response = {'status': 'ok'}
            elif request.get('type') == 'lookup':
                with self._lock:
                    entry = self._registry.get(request['name'])
                    if entry and (self.max_age is None or (time.time() - entry['timestamp']) <= self.max_age):
                        response = {'status': 'ok',
                                    'address': entry['address']}
                    else:
                        response = {'status': 'not_found'}
            else:
                response = {'status': 'error', 'message': 'invalid_request'}

            self._socket.sendto(pickle.dumps(response), addr)
        except Exception:
            pass

    def stop(self):
        '''Stop the nameserver.'''
        if not self._running:
            return

        self._running = False
        if self._socket:
            self._socket.close()
        if self._thread:
            self._thread.join()
