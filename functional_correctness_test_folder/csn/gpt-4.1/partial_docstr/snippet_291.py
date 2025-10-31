
import select


class SocketReceiver:

    def __init__(self):
        self._sockets = set()

    def register(self, socket):
        '''Register the socket.'''
        self._sockets.add(socket)

    def unregister(self, socket):
        self._sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        if sockets:
            sock_set = set(sockets)
        else:
            sock_set = self._sockets.copy()
        if not sock_set:
            return []
        rlist, _, _ = select.select(list(sock_set), [], [], timeout)
        return rlist
