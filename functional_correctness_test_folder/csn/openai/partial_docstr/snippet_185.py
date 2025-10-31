
class Transport:
    '''
    The transport I{interface}.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        self._is_open = False
        self._sent_messages = []

    def open(self, request):
        '''
        Open the transport. The `request` argument can contain any
        parameters needed to establish the connection. For this
        generic implementation we simply mark the transport as open.
        '''
        # In a real implementation you would use `request` to
        # configure the connection (e.g., host, port, credentials).
        self._is_open = True
        return True

    def send(self, request):
        '''
        Send a request over the transport. The `request` argument can be
        any serializable object. For this generic implementation we
        store the request in an internal list.
        '''
        if not self._is_open:
            raise RuntimeError("Transport is not open")
        self._sent_messages.append(request)
        return True

    # Optional helper methods for testing or debugging
    def is_open(self):
        return self._is_open

    def get_sent_messages(self):
        return list(self._sent_messages)
