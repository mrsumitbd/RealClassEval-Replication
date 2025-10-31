
class Transport:

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.connection = None
        self.kwargs = kwargs

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def send(self, message):
        if self.connection is None:
            raise ConnectionError("Not connected")
        self.connection.send(message)
