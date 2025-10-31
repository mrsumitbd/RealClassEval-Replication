
import socket


class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = {}
        for receiver in receivers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sockets[receiver] = sock

    def __call__(self, data):
        for receiver, sock in self.sockets.items():
            sock.sendto(data.encode(), (receiver, self.default_port))

    def close(self):
        '''Close the sender.'''
        for sock in self.sockets.values():
            sock.close()
