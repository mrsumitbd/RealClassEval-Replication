
import socket
import threading
import time
import logging


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.names = {}
        self.lock = threading.Lock()
        self.stopped = threading.Event()
        self.logger = logging.getLogger(__name__)

    def run(self, address_receiver=None, nameserver_address=None):
        '''Run the listener and answer to requests.'''
        if nameserver_address is None:
            nameserver_address = (
                '', 0) if self.restrict_to_localhost else ('', 9090)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(nameserver_address)
        nameserver_address = self.server_socket.getsockname()
        self.logger.info(f'NameServer listening on {nameserver_address}')

        if self.multicast_enabled:
            multicast_address = ('224.0.0.1', 9090)
            self.multicast_socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.multicast_socket.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            self.multicast_thread = threading.Thread(
                target=self._listen_multicast, args=(multicast_address,))
            self.multicast_thread.start()

        self.server_thread = threading.Thread(
            target=self._listen, args=(address_receiver,))
        self.server_thread.start()

        return nameserver_address

    def stop(self):
        '''Stop the nameserver.'''
        self.stopped.set()
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
        if hasattr(self, 'multicast_socket'):
            self.multicast_socket.close()
        if hasattr(self, 'server_thread'):
            self.server_thread.join()
        if hasattr(self, 'multicast_thread'):
            self.multicast_thread.join()

    def _listen(self, address_receiver=None):
        while not self.stopped.is_set():
            try:
                data, address = self.server_socket.recvfrom(1024)
                self.logger.debug(f'Received {data} from {address}')
                if data.decode().startswith('REGISTER'):
                    name = data.decode().split()[1]
                    with self.lock:
                        self.names[name] = (address, time.time())
                    if address_receiver:
                        address_receiver(name, address)
                elif data.decode().startswith('LOOKUP'):
                    name = data.decode().split()[1]
                    with self.lock:
                        if name in self.names:
                            response = self.names[name][0]
                            self.server_socket.sendto(
                                f'{response[0]} {response[1]}'.encode(), address)
                        else:
                            self.server_socket.sendto(
                                'NOTFOUND'.encode(), address)
                elif data.decode().startswith('LIST'):
                    with self.lock:
                        response = ' '.join(self.names.keys())
                        self.server_socket.sendto(response.encode(), address)
            except socket.error:
                if not self.stopped.is_set():
                    self.logger.error('Socket error occurred')

        self._clean_names()

    def _listen_multicast(self, multicast_address):
        self.multicast_socket.bind(multicast_address)
        self.multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                         socket.inet_aton('224.0.0.1') + socket.inet_aton('0.0.0.0'))
        while not self.stopped.is_set():
            try:
                data, address = self.multicast_socket.recvfrom(1024)
                self.logger.debug(f'Received multicast {data} from {address}')
                if data.decode().startswith('DISCOVER'):
                    self.multicast_socket.sendto(
                        f'NAMESERVER {self.server_socket.getsockname()[1]}'.encode(), address)
            except socket.error:
                if not self.stopped.is_set():
                    self.logger.error('Multicast socket error occurred')

    def _clean_names(self):
        with self.lock:
            current_time = time.time()
            self.names = {name: (address, timestamp) for name, (address, timestamp) in self.names.items()
                          if self.max_age is None or current_time - timestamp < self.max_age}
