
class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect_func = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.connection = None
        self.connected = False
        self.kwargs = kwargs
        self._connect()

    def _connect(self):
        try:
            self.connection = self.connect_func(
                self.gateway, timeout=self.timeout, **self.kwargs)
            self.connected = True
        except Exception as e:
            self.connection = None
            self.connected = False

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.connection and hasattr(self.connection, 'close'):
            try:
                self.connection.close()
            except Exception:
                pass
        self.connection = None
        self.connected = False

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.connected or self.connection is None:
            self._connect()
            if not self.connected:
                raise ConnectionError("Unable to connect to gateway.")
        try:
            if hasattr(self.connection, 'send'):
                self.connection.send(message)
            elif hasattr(self.connection, 'write'):
                self.connection.write(message)
            else:
                raise NotImplementedError(
                    "Connection object does not support send or write.")
        except Exception as e:
            self.connected = False
            raise
