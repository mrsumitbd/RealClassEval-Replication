
import socket
import struct


class MulticastSender:

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def __call__(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendto(data, (self.mcgroup, self.port)
                         if self.mcgroup else ('', self.port))

    def close(self):
        self.sock.close()
