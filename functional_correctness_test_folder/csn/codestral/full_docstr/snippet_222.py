
class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        '''Set up transport.'''
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs
        self.connection = None

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.connection:
            self.connection.close()
            self.connection = None

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.connection:
            self.connection = self.connect(
                self.gateway, timeout=self.timeout, **self.kwargs)
        try:
            self.connection.send(message)
        except Exception as e:
            self.disconnect()
            raise e
