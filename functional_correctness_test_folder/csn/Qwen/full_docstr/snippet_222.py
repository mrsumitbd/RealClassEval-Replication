
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
        self.connection = None
        self.connect_to_gateway()

    def connect_to_gateway(self):
        try:
            self.connection = self.connect(timeout=self.timeout)
        except Exception as e:
            print(f"Failed to connect to gateway: {e}")
            import time
            time.sleep(self.reconnect_timeout)
            self.connect_to_gateway()

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Failed to disconnect from gateway: {e}")
            finally:
                self.connection = None

    def send(self, message):
        '''Write a message to the gateway.'''
        if self.connection:
            try:
                self.connection.send(message)
            except Exception as e:
                print(f"Failed to send message: {e}")
                self.disconnect()
                self.connect_to_gateway()
        else:
            print("No active connection to send message.")
