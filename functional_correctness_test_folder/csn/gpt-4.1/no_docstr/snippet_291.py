
import select


class SocketReceiver:

    def __init__(self):
        self._sockets = set()

    def register(self, socket):
        self._sockets.add(socket)

    def unregister(self, socket):
        self._sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        if sockets:
            sockets_to_check = set(sockets)
        else:
            sockets_to_check = self._sockets.copy()
        if not sockets_to_check:
            return []
        readable, _, _ = select.select(list(sockets_to_check), [], [], timeout)
        return readable
