
import socket
import struct


class MulticastReceiver:

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup if mcgroup is not None else '224.0.0.1'
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('', self.port))
        except OSError:
            self.sock.bind(('0.0.0.0', self.port))
        mreq = struct.pack("4sl", socket.inet_aton(
            self.mcgroup), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def settimeout(self, tout=None):
        self.sock.settimeout(tout)

    def __call__(self):
        data, addr = self.sock.recvfrom(65536)
        return data, addr

    def close(self):
        self.sock.close()
