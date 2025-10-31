
import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self.default_port = default_port
        self.receivers = receivers
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __call__(self, data):
        '''Send messages from all receivers.'''
        for receiver in self.receivers:
            self.socket.sendto(data.encode(), (receiver, self.default_port))

    def close(self):
        '''Close the sender.'''
        self.socket.close()
