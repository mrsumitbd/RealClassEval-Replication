
class Transport:

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs
        self.connection = None

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def send(self, message):
        if self.connection is None:
            self.connection = self.connect(
                self.gateway, timeout=self.timeout, **self.kwargs)
        try:
            self.connection.send(message)
        except Exception as e:
            self.disconnect()
            raise e
