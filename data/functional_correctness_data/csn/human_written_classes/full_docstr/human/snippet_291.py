from posttroll.message import Message
import zmq

class SocketReceiver:
    """A receiver for mulitple sockets."""

    def __init__(self):
        """Set up the receiver."""
        self._poller = zmq.Poller()

    def register(self, socket):
        """Register the socket."""
        self._poller.register(socket, zmq.POLLIN)

    def unregister(self, socket):
        """Unregister the socket."""
        self._poller.unregister(socket)

    def receive(self, *sockets, timeout=None):
        """Timeout is in seconds."""
        if timeout:
            timeout *= 1000
        socks = dict(self._poller.poll(timeout=timeout))
        if socks:
            for sock in sockets:
                if socks.get(sock) == zmq.POLLIN:
                    received = sock.recv_string(zmq.NOBLOCK)
                    yield (Message.decode(received), sock)
        else:
            raise TimeoutError('Did not receive anything on sockets.')