
import socket
import threading
import time


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.services = {}
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def run(self, address_receiver=None, nameserver_address=None):
        '''Run the listener and answer to requests.'''
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._listen, args=(
            address_receiver, nameserver_address))
        self.thread.start()

    def stop(self):
        '''Stop the nameserver.'''
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def _listen(self, address_receiver, nameserver_address):
        if self.restrict_to_localhost:
            host = '127.0.0.1'
        else:
            host = ''
        port = 9999  # Default port for the name server

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            if self.multicast_enabled:
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(
                    '224.0.0.1') + socket.inet_aton(host))
                sock.bind(('224.0.0.1', port))
            else:
                sock.bind((host, port))

            while self.running:
                data, addr = sock.recvfrom(1024)
                if address_receiver:
                    address_receiver(data, addr)
                else:
                    self._handle_request(data, addr)

    def _handle_request(self, data, addr):
        request = data.decode('utf-8')
        if request.startswith('REGISTER'):
            _, name, service_address = request.split()
            with self.lock:
                self.services[name] = (service_address, time.time())
        elif request.startswith('LOOKUP'):
            _, name = request.split()
            with self.lock:
                if name in self.services:
                    service_address, timestamp = self.services[name]
                    if self.max_age is None or time.time() - timestamp < self.max_age:
                        response = f'FOUND {name} {service_address}'
                    else:
                        response = f'NOT_FOUND {name}'
                else:
                    response = f'NOT_FOUND {name}'
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(response.encode('utf-8'), addr)
