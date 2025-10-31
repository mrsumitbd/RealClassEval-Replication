
class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers
        self.connections = {receiver: None for receiver in receivers}

    def __call__(self, data):
        for receiver, connection in self.connections.items():
            if connection is None:
                # Establish connection logic here
                connection = self._establish_connection(
                    receiver, self.default_port)
                self.connections[receiver] = connection
            # Send data logic here
            self._send_data(connection, data)

    def close(self):
        '''Close the sender.'''
        for receiver, connection in self.connections.items():
            if connection is not None:
                # Close connection logic here
                self._close_connection(connection)
                self.connections[receiver] = None

    def _establish_connection(self, receiver, port):
        # Placeholder for connection establishment
        print(f"Establishing connection to {receiver} on port {port}")
        return f"Connection to {receiver}"

    def _send_data(self, connection, data):
        # Placeholder for sending data
        print(f"Sending data: {data} through {connection}")

    def _close_connection(self, connection):
        # Placeholder for closing connection
        print(f"Closing {connection}")
