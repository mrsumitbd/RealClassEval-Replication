import socket
import struct


class MulticastSender:
    '''Multicast sender on *port* and *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast sender.'''
        self.port = int(port)
        self.mcgroup = mcgroup or '224.0.0.1'
        self._closed = False

        if ':' in self.mcgroup:
            # IPv6 multicast
            self._family = socket.AF_INET6
            self._sock = socket.socket(self._family, socket.SOCK_DGRAM)
            try:
                self._sock.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)
                self._sock.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
            except OSError:
                pass
        else:
            # IPv4 multicast
            self._family = socket.AF_INET
            self._sock = socket.socket(self._family, socket.SOCK_DGRAM)
            try:
                self._sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except OSError:
                pass
            try:
                ttl = struct.pack('b', 1)
                self._sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                self._sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            except OSError:
                pass

    def __call__(self, data):
        if self._closed:
            raise RuntimeError("MulticastSender is closed")
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like or str")
        address = (self.mcgroup, self.port)
        return self._sock.sendto(data, address)

    def close(self):
        '''Close the sender.'''
        if not self._closed:
            try:
                self._sock.close()
            finally:
                self._closed = True
