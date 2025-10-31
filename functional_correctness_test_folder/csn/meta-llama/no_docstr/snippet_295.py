
import socket


class DesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = {}
        for receiver in receivers:
            self.sockets[receiver] = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)

    def __call__(self, data):
        for receiver, sock in self.sockets.items():
            try:
                sock.sendto(data, (receiver, self.default_port))
            except Exception as e:
                print(f"Error sending data to {receiver}: {e}")

    def close(self):
        for sock in self.sockets.values():
            sock.close()
        self.sockets = {}
