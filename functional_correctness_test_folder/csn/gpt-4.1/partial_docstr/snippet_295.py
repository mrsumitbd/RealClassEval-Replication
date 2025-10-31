
import socket


class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = []
        for r in receivers:
            if isinstance(r, tuple):
                self.receivers.append(r)
            else:
                self.receivers.append((r, self.default_port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.closed = False

    def __call__(self, data):
        if self.closed:
            raise RuntimeError("Sender is closed")
        if isinstance(data, str):
            data = data.encode()
        for addr, port in self.receivers:
            self.sock.sendto(data, (addr, port))

    def close(self):
        '''Close the sender.'''
        if not self.closed:
            self.sock.close()
            self.closed = True
