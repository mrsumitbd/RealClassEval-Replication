
import select


class SocketReceiver:

    def __init__(self):
        self.sockets = set()

    def register(self, socket):
        '''Register the socket.'''
        self.sockets.add(socket)

    def unregister(self, socket):
        if socket in self.sockets:
            self.sockets.remove(socket)

    def receive(self, *sockets, timeout=None):
        if not sockets:
            sockets = self.sockets
        else:
            sockets = [s for s in sockets if s in self.sockets]

        if not sockets:
            return []

        readable, _, _ = select.select(sockets, [], [], timeout)
        return readable
