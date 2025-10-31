
import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        if mcgroup is None:
            mcgroup = '224.0.0.1'
        self.mcgroup = mcgroup
        self.port = port
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
        self.closed = False

    def __call__(self, data):
        if self.closed:
            raise ValueError("Sender is closed")
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        if not self.closed:
            self.sock.close()
            self.closed = True
