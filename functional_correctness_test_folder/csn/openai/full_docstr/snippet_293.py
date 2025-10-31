
import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        if mcgroup is None:
            # Default multicast group
            mcgroup = '224.0.0.1'
        self.port = port
        self.mcgroup = mcgroup

        # Create UDP socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Set TTL to 1 (local network)
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def __call__(self, data):
        '''Send data to a socket.'''
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        try:
            self.sock.close()
        except Exception:
            pass
