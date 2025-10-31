
import socket
import struct


class MulticastSender:

    def __init__(self, port, mcgroup='224.1.1.1'):
        """
        Initialize a MulticastSender.

        Args:
            port (int): The port to send multicast data on.
            mcgroup (str, optional): The multicast group to send data to. Defaults to '224.1.1.1'.
        """
        self.port = port
        self.mcgroup = mcgroup
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __call__(self, data):
        """
        Send data to the multicast group.

        Args:
            data (bytes): The data to be sent.
        """
        self.sock.sendto(data, (self.mcgroup, self.port))

    def close(self):
        """
        Close the socket.
        """
        self.sock.close()


# Example usage:
if __name__ == "__main__":
    sender = MulticastSender(12345)
    sender(b'Hello, world!')
    sender.close()
