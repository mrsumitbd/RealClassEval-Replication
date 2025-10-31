
import socket
import struct
import sys


class MulticastReceiver:
    '''Multicast receiver on *port* for an *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        '''Set up the multicast receiver.'''
        # Create a UDP socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the port on all interfaces
        try:
            self.sock.bind(('', port))
        except OSError as e:
            self.sock.close()
            raise e

        # Join the multicast group if requested
        if mcgroup:
            # Convert the multicast group address to binary form
            mcast_grp = socket.inet_aton(mcgroup)
            # Use INADDR_ANY for the interface address
            local_addr = socket.inet_aton('0.0.0.0')
            mreq = struct.pack('4s4s', mcast_grp, local_addr)
            try:
                self.sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            except OSError as e:
                self.sock.close()
                raise e

        # Default timeout is None (blocking)
        self.timeout = None

    def settimeout(self, tout=None):
        '''Set timeout.
        A timeout will throw a 'socket.timeout'.
        '''
        self.timeout = tout
        self.sock.settimeout(tout)

    def __call__(self):
        '''Receive data from a socket.'''
        try:
            data, addr = self.sock.recvfrom(65535)
            return data, addr
        except socket.timeout:
            raise
        except OSError as e:
            # If the socket is closed or other error occurs
            raise e

    def close(self):
        '''Close the receiver.'''
        try:
            self.sock.close()
        except OSError:
            pass
