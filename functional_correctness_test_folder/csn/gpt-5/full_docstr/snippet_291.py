import select


class SocketReceiver:
    '''A receiver for mulitple sockets.'''

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
        read_set = set(sockets) if sockets else set(self._sockets)
        if not read_set:
            return {}
        try:
            ready, _, _ = select.select(list(read_set), [], [], timeout)
        except Exception:
            return {}
        results = {}
        for s in ready:
            try:
                data = s.recv(4096)
            except BlockingIOError:
                continue
            except Exception:
                self.unregister(s)
                results[s] = None
                continue
            if data == b'':
                self.unregister(s)
            results[s] = data
        return results
