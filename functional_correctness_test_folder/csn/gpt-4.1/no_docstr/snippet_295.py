
import socket


class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.closed = False

    def __call__(self, data):
        if self.closed:
            raise RuntimeError("Socket is closed")
        if isinstance(data, str):
            data = data.encode()
        for receiver in self.receivers:
            if isinstance(receiver, tuple):
                host, port = receiver
            else:
                host, port = receiver, self.default_port
            self.sock.sendto(data, (host, port))

    def close(self):
        if not self.closed:
            self.sock.close()
            self.closed = True
