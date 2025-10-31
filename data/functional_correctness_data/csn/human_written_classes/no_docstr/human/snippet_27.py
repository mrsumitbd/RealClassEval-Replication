import socket

class _RemoteSocket:

    def acquire(self) -> int:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))
        return self.socket.getsockname()[1]

    def release(self) -> None:
        self.socket.close()