class MulticastSender:
    """Multicast sender on *port* and *mcgroup*."""

    def __init__(self, port, mcgroup=None):
        """Set up the multicast sender."""
        self.port = port
        self.group = mcgroup
        self.socket, self.group = mcast_sender(mcgroup)
        logger.debug('Started multicast group %s', self.group)

    def __call__(self, data):
        """Send data to a socket."""
        self.socket.sendto(data.encode(), (self.group, self.port))

    def close(self):
        """Close the sender."""
        self.socket.close()