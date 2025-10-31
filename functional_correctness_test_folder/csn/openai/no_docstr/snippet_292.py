
import socket
import struct


class MulticastReceiver:
    """
    A simple multicast UDP receiver.

    Parameters
    ----------
    port : int
        The UDP port to bind to.
    mcgroup : str, optional
        The multicast group address to join. If None, defaults to
        '224.0.0.1'.
    """

    def __init__(self, port, mcgroup=None):
        self.port = port
        self.mcgroup = mcgroup or '224.0.0.1'
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to the port on all interfaces
        self.sock.bind(('', self.port))
        # Join the multicast group
        mreq = struct.pack("4sL", socket.inet_aton(
            self.mcgroup), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.timeout = None

    def settimeout(self, tout=None):
        """
        Set the socket timeout.

        Parameters
        ----------
        tout : float or None
            Timeout in seconds. If None, the socket is blocking.
        """
        self.timeout = tout
        self.sock.settimeout(tout)

    def __call__(self):
        """
        Receive a single datagram from the multicast group.

        Returns
        -------
        data : bytes
            The received payload.
        addr : tuple
            The address of the sender.
        """
        try:
            data, addr = self.sock.recvfrom(65535)
            return data, addr
        except socket.timeout:
            return None, None
        except OSError:
            return None, None

    def close(self):
        """
        Leave the multicast group and close the socket.
        """
        try:
            mreq = struct.pack("4sL", socket.inet_aton(
                self.mcgroup), socket.INADDR_ANY)
            self.sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        finally:
            self.sock.close()
