
import select
import socket


class SocketReceiver:
    '''A receiver for multiple sockets.'''

    def __init__(self):
        '''Set up the receiver.'''
        self._sockets = set()

    def register(self, sock):
        '''Register the socket.'''
        if not isinstance(sock, socket.socket):
            raise TypeError("Only socket.socket instances can be registered")
        self._sockets.add(sock)

    def unregister(self, sock):
        '''Unregister the socket.'''
        self._sockets.discard(sock)

    def receive(self, *sockets, timeout=None):
        '''Receive data from the given sockets or all registered sockets.
        Timeout is in seconds. Returns a list of (socket, data) tuples.'''
        # Determine which sockets to monitor
        if sockets:
            read_socks = list(sockets)
        else:
            read_socks = list(self._sockets)

        if not read_socks:
            return []

        # Use select to wait for readability
        try:
            readable, _, exceptional = select.select(
                read_socks, [], read_socks, timeout)
        except (ValueError, select.error):
            # If any socket is invalid, remove it and retry
            for s in read_socks:
                if s not in self._sockets:
                    continue
                try:
                    s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                except socket.error:
                    self.unregister(s)
            return []

        results = []
        for sock in readable:
            try:
                data = sock.recv(4096)
                if data:
                    results.append((sock, data))
                else:
                    # No data means the socket has been closed
                    self.unregister(sock)
            except socket.error:
                # On error, unregister the socket
                self.unregister(sock)

        # Handle exceptional sockets
        for sock in exceptional:
            self.unregister(sock)

        return results
