
import time


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
        self.connected = False
        self.last_connect_time = None
        self.kwargs = kwargs

    def disconnect(self):
        '''Disconnect from the transport.'''
        self.connected = False

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.connected:
            raise ConnectionError("Not connected to the gateway")
        # Simulate sending the message (actual implementation would depend on the transport)
        print(f"Sending message to {self.gateway}: {message}")
