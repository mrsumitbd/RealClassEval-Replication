
class Transport:

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.connection = None
        self.connect_to_gateway()

    def connect_to_gateway(self):
        try:
            self.connection = self.connect(self.gateway, timeout=self.timeout)
        except Exception as e:
            print(f"Failed to connect to {self.gateway}: {e}")
            import time
            time.sleep(self.reconnect_timeout)
            self.connect_to_gateway()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def send(self, message):
        if self.connection:
            try:
                self.connection.send(message)
            except Exception as e:
                print(f"Failed to send message: {e}")
                self.disconnect()
                self.connect_to_gateway()
                self.send(message)
        else:
            print("Not connected to gateway. Reconnecting...")
            self.connect_to_gateway()
            self.send(message)
