import socket

class UDPSocketTransport:

    def __init__(self, address, timeout):
        self.socket = None
        self.address = address
        self.timeout = timeout
        self.open()

    def open(self):
        error = None
        host, port = self.address
        addrinfo = socket.getaddrinfo(host, port, 0, socket.SOCK_DGRAM)
        if not addrinfo:
            raise OSError('getaddrinfo returns an empty list')
        for entry in addrinfo:
            family, socktype, _, _, sockaddr = entry
            try:
                self.socket = socket.socket(family, socktype)
                self.socket.settimeout(self.timeout)
                self.address = sockaddr
                break
            except OSError as e:
                error = e
                if self.socket is not None:
                    self.socket.close()
        if error is not None:
            raise error

    def transmit(self, syslog_msg):
        try:
            self.socket.sendto(syslog_msg, self.address)
        except (OSError, IOError):
            self.close()
            self.open()
            self.socket.sendto(syslog_msg, self.address)

    def close(self):
        self.socket.close()