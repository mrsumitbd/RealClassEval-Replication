
import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = {}
        for receiver in receivers:
            self.sockets[receiver] = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)

    def __call__(self, data):
        '''Send messages from all receivers.'''
        for receiver, sock in self.sockets.items():
            try:
                sock.sendto(data.encode(), (receiver, self.default_port))
            except Exception as e:
                print(f"Error sending to {receiver}: {e}")

    def close(self):
        '''Close the sender.'''
        for sock in self.sockets.values():
            sock.close()
        self.sockets = {}


# Example usage:
if __name__ == "__main__":
    receivers = ["127.0.0.1", "192.168.1.100"]
    port = 12345
    sender = DesignatedReceiversSender(port, receivers)
    sender("Hello, world!")
    sender.close()
