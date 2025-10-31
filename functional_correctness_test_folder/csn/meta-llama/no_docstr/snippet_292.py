
import socket
import struct


class MulticastReceiver:

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup if mcgroup else '224.1.1.1'
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        mreq = struct.pack("4sl", socket.inet_aton(
            self.mcgroup), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def settimeout(self, tout=None):
        self.sock.settimeout(tout)

    def __call__(self):
        try:
            data, address = self.sock.recvfrom(1024)
            return data, address
        except socket.timeout:
            return None, None

    def close(self):
        self.sock.close()
