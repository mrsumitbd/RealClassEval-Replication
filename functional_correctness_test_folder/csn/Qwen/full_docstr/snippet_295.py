
import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = []

    def __call__(self, data):
        '''Send messages from all receivers.'''
        for receiver in self.receivers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((receiver, self.default_port))
            sock.sendall(data.encode())
            self.sockets.append(sock)

    def close(self):
        '''Close the sender.'''
        for sock in self.sockets:
            sock.close()
        self.sockets = []
