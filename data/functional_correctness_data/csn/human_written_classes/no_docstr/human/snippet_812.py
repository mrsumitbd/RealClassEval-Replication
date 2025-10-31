import socket

class UnixSocketTransport:

    def __init__(self, address, socket_type):
        self.socket = None
        self.address = address
        self.socket_type = socket_type
        self.open()

    def open(self):
        if self.socket_type is None:
            socket_types = [socket.SOCK_DGRAM, socket.SOCK_STREAM]
        else:
            socket_types = [self.socket_type]
        for type_ in socket_types:
            try:
                self.socket = socket.socket(socket.AF_UNIX, type_)
                self.socket.connect(self.address)
                self.socket_type = type_
                break
            except OSError:
                if self.socket is not None:
                    self.socket.close()

    def transmit(self, syslog_msg):
        try:
            self.socket.send(syslog_msg)
        except (OSError, IOError):
            self.close()
            self.open()
            self.socket.send(syslog_msg)

    def close(self):
        self.socket.close()