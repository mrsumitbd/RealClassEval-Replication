
import socket
import struct


class MulticastSender:

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup if mcgroup is not None else '224.0.0.1'
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Set TTL to 1 so the multicast doesn't go past the local network
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.address = (self.mcgroup, self.port)
        self.closed = False

    def __call__(self, data):
        if self.closed:
            raise ValueError("Socket is closed")
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendto(data, self.address)

    def close(self):
        if not self.closed:
            self.sock.close()
            self.closed = True
