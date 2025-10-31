
import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = []

        for receiver in receivers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sockets.append(sock)

    def __call__(self, data):
        '''Send messages from all receivers.'''
        for i, receiver in enumerate(self.receivers):
            self.sockets[i].sendto(
                data.encode(), (receiver, self.default_port))

    def close(self):
        '''Close the sender.'''
        for sock in self.sockets:
            sock.close()
