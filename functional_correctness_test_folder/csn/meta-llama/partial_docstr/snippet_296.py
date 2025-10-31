
import socket
import threading
import logging


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._names = {}
        self._lock = threading.Lock()
        self._socket = None
        self._stop_event = threading.Event()

    def run(self, address_receiver=None, nameserver_address=None):
        if nameserver_address is None:
            nameserver_address = (
                '', 9091) if self.restrict_to_localhost else ('', 9090)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(nameserver_address)

        if self.multicast_enabled:
            multicast_address = ('224.3.29.71', 9090)
            self._socket.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                    socket.inet_aton(multicast_address[0]) + socket.inet_aton('0.0.0.0'))

        logging.info(f'Name server started on {nameserver_address}')

        while not self._stop_event.is_set():
            try:
                data, address = self._socket.recvfrom(1024)
                if address_receiver:
                    address_receiver(address)
                request = data.decode().split(':')
                if request[0] == 'register':
                    with self._lock:
                        self._names[request[1]] = (address[0], int(request[2]))
                        if self.max_age:
                            threading.Timer(
                                self.max_age, self._remove_name, args=(request[1],)).start()
                elif request[0] == 'lookup':
                    with self._lock:
                        if request[1] in self._names:
                            response = f'{self._names[request[1]][0]}:{self._names[request[1]][1]}'
                            self._socket.sendto(response.encode(), address)
            except socket.timeout:
                continue
            except Exception as e:
                logging.error(f'Error occurred: {e}')

    def stop(self):
        self._stop_event.set()
        if self._socket:
            self._socket.close()
        logging.info('Name server stopped')

    def _remove_name(self, name):
        with self._lock:
            if name in self._names:
                del self._names[name]
