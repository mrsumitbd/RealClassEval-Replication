
import select
import socket


class SocketReceiver:
    def __init__(self):
        # Store registered sockets in a set for quick lookup
        self._registered = set()

    def register(self, sock):
        """Register a socket to be monitored."""
        if not isinstance(sock, socket.socket):
            raise TypeError("Only socket.socket instances can be registered")
        self._registered.add(sock)

    def unregister(self, sock):
        """Unregister a previously registered socket."""
        self._registered.discard(sock)

    def receive(self, *sockets, timeout=None):
        """
        Wait for any of the given sockets (or all registered sockets if none are given)
        to become readable. Returns a list of (socket, data) tuples.
        If a socket is closed (recv returns b''), it is automatically unregistered.
        """
        # Determine which sockets to monitor
        if sockets:
            read_list = list(sockets)
        else:
            read_list = list(self._registered)

        if not read_list:
            return []

        # Use select to wait for readability
        try:
            ready, _, _ = select.select(read_list, [], [], timeout)
        except select.error as e:
            raise RuntimeError(f"Select error: {e}")

        results = []
        for sock in ready:
            try:
                data = sock.recv(4096)
            except socket.error:
                # On error, skip this socket
                continue
            if data:
                results.append((sock, data))
            else:
                # Empty data means the socket has been closed
                self.unregister(sock)
        return results
