import socket

class TCPSocketTransport:

    def __init__(self, address, timeout, framing):
        self.socket = None
        self.address = address
        self.timeout = timeout
        self.framing = framing
        self.open()

    def open(self):
        error = None
        host, port = self.address
        addrinfo = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
        if not addrinfo:
            raise OSError('getaddrinfo returns an empty list')
        for entry in addrinfo:
            family, socktype, _, _, sockaddr = entry
            try:
                self.socket = socket.socket(family, socktype)
                self.socket.settimeout(self.timeout)
                self.socket.connect(sockaddr)
                error = None
                break
            except OSError as e:
                error = e
                if self.socket is not None:
                    self.socket.close()
        if error is not None:
            raise error

    def transmit(self, syslog_msg):
        if self.framing == FRAMING_NON_TRANSPARENT:
            syslog_msg = syslog_msg.replace(b'\n', b'\\n')
            syslog_msg = b''.join((syslog_msg, b'\n'))
        else:
            syslog_msg = b' '.join((str(len(syslog_msg)).encode('ascii'), syslog_msg))
        try:
            self.socket.sendall(syslog_msg)
        except (OSError, IOError):
            self.close()
            self.open()
            self.socket.sendall(syslog_msg)

    def close(self):
        self.socket.close()