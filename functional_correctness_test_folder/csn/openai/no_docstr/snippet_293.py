
import socket
import struct


class MulticastSender:
    """
    Simple UDP multicast sender.

    Parameters
    ----------
    port : int
        Destination port for the multicast packets.
    mcgroup : str, optional
        Multicast group address. Defaults to '224.0.0.1'.
    ttl : int, optional
        Time-to-live for multicast packets. Defaults to 1.
    """

    def __init__(self, port, mcgroup=None, ttl=1):
        self.port = port
        self.mcgroup = mcgroup or '224.0.0.1'
        self.ttl = ttl

        # Create a UDP socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Set the TTL for multicast packets
        ttl_bin = struct.pack('b', self.ttl)
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

        # Disable loopback so we don't receive our own packets
        self.sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, b'\x00')

    def __call__(self, data):
        """
        Send data to the multicast group.

        Parameters
        ----------
        data : bytes or str
            The payload to send. If a string is provided, it will be encoded as UTF-8.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes, bytearray, or str")

        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        """Close the underlying socket."""
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None
