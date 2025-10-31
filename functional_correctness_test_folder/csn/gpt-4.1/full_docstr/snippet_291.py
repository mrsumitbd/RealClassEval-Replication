
import select


class SocketReceiver:
    '''A receiver for multiple sockets.'''

    def __init__(self):
        '''Set up the receiver.'''
        self._sockets = set()

    def register(self, socket):
        '''Register the socket.'''
        self._sockets.add(socket)

    def unregister(self, socket):
        '''Unregister the socket.'''
        self._sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        '''Timeout is in seconds.'''
        if sockets:
            sockset = set(sockets)
        else:
            sockset = self._sockets
        if not sockset:
            return []
        readable, _, _ = select.select(list(sockset), [], [], timeout)
        return readable
