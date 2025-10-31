
import socket
import struct


class MulticastReceiver:
    '''Multicast receiver on *port* for an *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast receiver.'''
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('' if mcgroup is None else mcgroup, port))
        if mcgroup is not None:
            mreq = struct.pack('4sl', socket.inet_aton(
                mcgroup), socket.INADDR_ANY)
            self.sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def settimeout(self, tout=None):
        '''Set timeout.
        A timeout will throw a 'socket.timeout'.
        '''
        self.sock.settimeout(tout)

    def __call__(self):
        '''Receive data from a socket.'''
        return self.sock.recv(65536)

    def close(self):
        '''Close the receiver.'''
        self.sock.close()
