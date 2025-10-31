import struct
from socket import AF_INET, INADDR_ANY, IP_ADD_MEMBERSHIP, IP_MULTICAST_IF, IP_MULTICAST_LOOP, IP_MULTICAST_TTL, IPPROTO_IP, SO_BROADCAST, SO_LINGER, SO_REUSEADDR, SOCK_DGRAM, SOL_IP, SOL_SOCKET, gethostbyname, inet_aton, socket, timeout

class MulticastReceiver:
    """Multicast receiver on *port* for an *mcgroup*."""
    BUFSIZE = 1024

    def __init__(self, port, mcgroup=None):
        """Set up the multicast receiver."""
        self.port = port
        self.socket, self.group = mcast_receiver(port, mcgroup)
        logger.info(f'Receiver initialized on group {self.group}.')

    def settimeout(self, tout=None):
        """Set timeout.

        A timeout will throw a 'socket.timeout'.
        """
        self.socket.settimeout(tout)
        return self

    def __call__(self):
        """Receive data from a socket."""
        data, sender = self.socket.recvfrom(self.BUFSIZE)
        return (data.decode(), sender)

    def close(self):
        """Close the receiver."""
        self.socket.setsockopt(SOL_SOCKET, SO_LINGER, struct.pack('ii', 1, 1))
        self.socket.close()