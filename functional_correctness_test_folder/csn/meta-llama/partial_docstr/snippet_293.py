
import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup='224.0.0.1'):
        '''Set up the multicast sender.'''
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __call__(self, data):
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        self.sock.close()
