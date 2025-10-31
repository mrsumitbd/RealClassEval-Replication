
import socket
import threading
import time


class NameServer:

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

        if nameserver_address:
            host, port = nameserver_address
        else:
            port = 9999

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((host, port))
            if self.multicast_enabled:
                mreq = struct.pack("4sl", socket.inet_aton(
                    '224.0.0.1'), socket.INADDR_ANY)
                sock.setsockopt(socket.IPPROTO_IP,
                                socket.IP_ADD_MEMBERSHIP, mreq)

            while self.running:
                data, addr = sock.recvfrom(1024)
                if address_receiver:
                    address_receiver(data, addr)
                else:
                    self._handle_message(data, addr)

    def _handle_message(self, data, addr):
        with self.lock:
            service_info = data.decode().split(',')
            service_name, service_address, service_port = service_info[0], service_info[1], int(
                service_info[2])
            self.services[service_name] = (
                service_address, service_port, time.time())

            if self.max_age:
                self._cleanup_services()

    def _cleanup_services(self):
        current_time = time.time()
        with self.lock:
            to_remove = [name for name, (_, _, timestamp) in self.services.items(
            ) if current_time - timestamp > self.max_age]
            for name in to_remove:
                del self.services[name]
