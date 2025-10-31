
class Transport:

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs
        self.connected = False

    def disconnect(self):
        self.connected = False

    def send(self, message):
        if not self.connected:
            self.connected = True  # Simulate connecting
        # Simulate sending message
        return f"Message sent to {self.gateway}: {message}"
