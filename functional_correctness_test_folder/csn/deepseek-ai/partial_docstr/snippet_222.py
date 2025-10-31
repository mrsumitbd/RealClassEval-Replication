
class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.connection = None
        self._setup_connection()

    def _setup_connection(self):
        if self.connect:
            try:
                self.connection = self._establish_connection()
            except Exception as e:
                print(f"Connection failed: {e}")
                self.connection = None

    def _establish_connection(self):
        return f"Connection to {self.gateway}"

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.connection:
            print(f"Disconnecting from {self.gateway}")
            self.connection = None

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.connection:
            raise ConnectionError("Not connected to the gateway")
        print(f"Sending message: {message} to {self.gateway}")
