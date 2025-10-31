
import socket
import threading


class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        self.subscriber = subscriber
        self.services = services.split(',')
        self.nameserver = nameserver
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', 7401))
        self.multicast_group = '224.0.0.1'
        self.multicast_port = 7400
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('0.0.0.0'))
        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            self.handle_msg(data.decode('utf-8'))

    def handle_msg(self, msg):
        parts = msg.split(',')
        if len(parts) < 3:
            return
        service = parts[0]
        if service in self.services or not self.services:
            self.subscriber(service, parts[1], int(parts[2]))
