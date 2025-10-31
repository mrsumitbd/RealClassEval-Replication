
import select


class SocketReceiver:

    def __init__(self):
        self._sockets = set()

    def register(self, socket):
        self._sockets.add(socket)

    def unregister(self, socket):
        self._sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        if not sockets:
            sockets = self._sockets
        else:
            sockets = [s for s in sockets if s in self._sockets]

        if not sockets:
            return []

        ready, _, _ = select.select(sockets, [], [], timeout)
        return ready
