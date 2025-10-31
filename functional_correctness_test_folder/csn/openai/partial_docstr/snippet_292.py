
import socket
import struct


class MulticastReceiver:
    '''Multicast receiver on *port* for an *mcgroup*.'''

    def __init__(self, port, mcgroup=None):
        # Default multicast group if none provided
        if mcgroup is None:
            mcgroup = '224.0.0.1'
        self.port = port
        self.mcgroup = mcgroup

        # Create UDP socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the port on all interfaces
        self.sock.bind(('', self.port))

        # Join the multicast group
        mreq = struct.pack("4s4s", socket.inet_aton(
            self.mcgroup), socket.inet_aton('0.0.0.0'))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Default timeout is None (blocking)
        self.tout = None

    def settimeout(self, tout=None):
        '''Set timeout.
        A timeout will throw a 'socket.timeout'.
        '''
        self.tout = tout
        self.sock.settimeout(tout)

    def __call__(self):
        '''Receive a single datagram. Returns (data, address).'''
        try:
            data, addr = self.sock.recvfrom(65535)
            return data, addr
        except socket.timeout:
            raise
        except OSError as e:
            # Re-raise as socket.error for consistency
            raise socket.error(e)

    def close(self):
        '''Close the receiver.'''
        try:
            # Leave the multicast group before closing
            mreq = struct.pack("4s4s", socket.inet_aton(
                self.mcgroup), socket.inet_aton('0.0.0.0'))
            self.sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        finally:
            self.sock.close()
