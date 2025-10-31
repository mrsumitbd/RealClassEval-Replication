
import socket


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __call__(self, data):
        if self.mcgroup:
            self.sock.sendto(data.encode(), (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        self.sock.close()
