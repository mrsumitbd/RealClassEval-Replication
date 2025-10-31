
import select


class SocketReceiver:
    '''A receiver for multiple sockets.'''

    def __init__(self):
        '''Set up the receiver.'''
        self.sockets = set()

    def register(self, socket):
        '''Register the socket.'''
        self.sockets.add(socket)

    def unregister(self, socket):
        '''Unregister the socket.'''
        self.sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        '''Timeout is in seconds.'''
        if not sockets:
            sockets = self.sockets
        else:
            sockets = [s for s in sockets if s in self.sockets]
        if not sockets:
            return []
        readable, _, _ = select.select(sockets, [], [], timeout)
        return readable
