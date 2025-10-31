import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        if not isinstance(port, int):
            raise TypeError("port must be an integer")
        self.port = port
        self.mcgroup = mcgroup or '224.0.0.1'
        if not isinstance(self.mcgroup, str):
            raise TypeError("mcgroup must be a string IP address")
        # Create UDP socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Set TTL to 1 (local network)
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        # Disable loopback so we don't receive our own packets
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

    def __call__(self, data):
        if self.sock is None:
            raise ValueError("Socket is closed")
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or str")
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        '''Close the sender.'''
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None
        return None
