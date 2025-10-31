
import socket
import struct


class MulticastSender:

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __call__(self, data):
        if self.mcgroup is not None:
            self.sock.sendto(data.encode(), (self.mcgroup, self.port))

    def close(self):
        self.sock.close()
