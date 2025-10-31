import socket
import struct


class MulticastReceiver:
    '''Multicast receiver on *port* for an *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        self.port = int(port)
        self.mcgroup = mcgroup
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError:
            pass
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass
        self.sock.bind(('', self.port))
        if self.mcgroup:
            mreq = struct.pack('=4s4s', socket.inet_aton(
                self.mcgroup), socket.inet_aton('0.0.0.0'))
            self.sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def settimeout(self, tout=None):
        '''Set timeout.
        A timeout will throw a 'socket.timeout'.
        '''
        if self.sock is None:
            raise RuntimeError("Receiver is closed")
        self.sock.settimeout(tout)

    def __call__(self):
        if self.sock is None:
            raise RuntimeError("Receiver is closed")
        data, addr = self.sock.recvfrom(65535)
        return data, addr

    def close(self):
        '''Close the receiver.'''
        if self.sock is not None:
            try:
                if self.mcgroup:
                    mreq = struct.pack('=4s4s', socket.inet_aton(
                        self.mcgroup), socket.inet_aton('0.0.0.0'))
                    try:
                        self.sock.setsockopt(
                            socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
                    except OSError:
                        pass
            finally:
                try:
                    self.sock.close()
                finally:
                    self.sock = None
