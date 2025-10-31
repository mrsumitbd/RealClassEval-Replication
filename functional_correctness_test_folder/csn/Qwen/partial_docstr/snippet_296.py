
import socket
import threading
import time


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.services = {}
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def run(self, address_receiver=None, nameserver_address=None):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_server, args=(
            address_receiver, nameserver_address))
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.thread.join()

    def _run_server(self, address_receiver, nameserver_address):
        if self.restrict_to_localhost:
            host = '127.0.0.1'
        else:
            host = ''
        port = 9999 if nameserver_address is None else nameserver_address[1]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            if self.multicast_enabled:
                mreq = struct.pack("4sl", socket.inet_aton(
                    "224.0.0.1"), socket.INADDR_ANY)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            while self.running:
                data, addr = s.recvfrom(1024)
                with self.lock:
                    self._handle_message(data, addr)
                if self.max_age:
                    self._cleanup_services()

    def _handle_message(self, data, addr):
        message = data.decode('utf-8')
        if message.startswith('REGISTER'):
            _, name, service_address = message.split(' ', 2)
            self.services[name] = (service_address, time.time())
        elif message.startswith('LOOKUP'):
            _, name = message.split(' ', 1)
            if name in self.services:
                service_address, _ = self.services[name]
                response = f"SERVICE {name} {service_address}"
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(response.encode('utf-8'), addr)

    def _cleanup_services(self):
        current_time = time.time()
        to_remove = [name for name, (_, timestamp) in self.services.items(
        ) if current_time - timestamp > self.max_age]
        for name in to_remove:
            del self.services[name]
