import socket
import struct


class MulticastReceiver:
    def __init__(self, port, mcgroup=None):
        self._sock = None
        self._af = socket.AF_INET
        self._port = int(port)
        self._mcgroup = mcgroup
        self._timeout = None

        if mcgroup and ':' in mcgroup:
            self._af = socket.AF_INET6

        self._sock = socket.socket(self._af, socket.SOCK_DGRAM)

        try:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError:
            pass
        try:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass

        if self._af == socket.AF_INET6:
            bind_addr = '::'
            try:
                self._sock.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            except OSError:
                pass
        else:
            bind_addr = '0.0.0.0'

        self._sock.bind((bind_addr, self._port))

        if self._mcgroup:
            if self._af == socket.AF_INET:
                mreq = struct.pack('=4s4s', socket.inet_aton(
                    self._mcgroup), socket.inet_aton('0.0.0.0'))
                self._sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            else:
                group_bin = socket.inet_pton(socket.AF_INET6, self._mcgroup)
                mreq6 = struct.pack('=16sI', group_bin, 0)
                self._sock.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq6)

    def settimeout(self, tout=None):
        self._timeout = tout
        self._sock.settimeout(tout)

    def __call__(self):
        return self._sock.recvfrom(65535)

    def close(self):
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None
