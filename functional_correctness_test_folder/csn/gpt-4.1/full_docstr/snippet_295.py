
import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self.default_port = default_port
        self.receivers = receivers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __call__(self, data):
        '''Send messages from all receivers.'''
        if isinstance(data, str):
            data = data.encode('utf-8')
        for receiver in self.receivers:
            if isinstance(receiver, tuple):
                host, port = receiver
            else:
                host, port = receiver, self.default_port
            self.sock.sendto(data, (host, port))

    def close(self):
        '''Close the sender.'''
        self.sock.close()
