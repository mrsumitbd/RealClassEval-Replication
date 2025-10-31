
import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        self.port = port
        self.mcgroup = mcgroup if mcgroup is not None else '224.1.1.1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def __call__(self, data):
        '''Send *data* to the multicast group.'''
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        self.sock.close()
