import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        self.port = int(port)
        self.mcgroup = mcgroup or '224.0.0.1'
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self._sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('B', 1))
        except OSError:
            self._sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    def __call__(self, data):
        '''Send data to a socket.'''
        if self._sock is None:
            raise RuntimeError("Sender is closed")
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self._sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None
