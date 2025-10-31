import socket
import struct


class MulticastReceiver:
    '''Multicast receiver on *port* for an *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast receiver.'''
        self.port = int(port)
        self.mcgroup = mcgroup
        self.sock = None
        self._family = socket.AF_INET
        self._joined = False
        self._iface_index = 0

        if mcgroup and ':' in mcgroup:
            self._family = socket.AF_INET6

        self.sock = socket.socket(self._family, socket.SOCK_DGRAM)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError:
            pass
        try:
            # Not available on all platforms
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass

        if self._family == socket.AF_INET6:
            self.sock.bind(('', self.port))
            if mcgroup:
                grp_bin = socket.inet_pton(socket.AF_INET6, mcgroup)
                mreq = struct.pack('16sI', grp_bin, self._iface_index)
                self.sock.setsockopt(socket.IPPROTO_IPV6,
                                     socket.IPV6_JOIN_GROUP, mreq)
                self._joined = True
        else:
            self.sock.bind(('', self.port))
            if mcgroup:
                mreq = struct.pack('=4s4s',
                                   socket.inet_aton(mcgroup),
                                   socket.inet_aton('0.0.0.0'))
                self.sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                self._joined = True

    def settimeout(self, tout=None):
        '''Set timeout.
        A timeout will throw a 'socket.timeout'.
        '''
        self.sock.settimeout(tout)

    def __call__(self):
        '''Receive data from a socket.'''
        return self.sock.recvfrom(65535)

    def close(self):
        '''Close the receiver.'''
        try:
            if self._joined and self.mcgroup and self.sock:
                if self._family == socket.AF_INET6:
                    grp_bin = socket.inet_pton(socket.AF_INET6, self.mcgroup)
                    mreq = struct.pack('16sI', grp_bin, self._iface_index)
                    try:
                        self.sock.setsockopt(
                            socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
                    except OSError:
                        pass
                else:
                    mreq = struct.pack('=4s4s',
                                       socket.inet_aton(self.mcgroup),
                                       socket.inet_aton('0.0.0.0'))
                    try:
                        self.sock.setsockopt(
                            socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
                    except OSError:
                        pass
        finally:
            if self.sock:
                try:
                    self.sock.close()
                finally:
                    self.sock = None
