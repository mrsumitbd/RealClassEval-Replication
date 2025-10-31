
class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers
        self.connections = {receiver: None for receiver in receivers}

    def __call__(self, data):
        for receiver, connection in self.connections.items():
            if connection is None:
                # Simulate establishing a connection
                connection = f"Connection to {receiver} on port {self.default_port}"
                self.connections[receiver] = connection
            # Simulate sending data
            print(f"Sending data to {receiver} via {connection}: {data}")

    def close(self):
        for receiver, connection in self.connections.items():
            if connection is not None:
                # Simulate closing the connection
                print(f"Closing connection to {receiver}")
                self.connections[receiver] = None
