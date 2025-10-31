import socket
import struct
import ipaddress


class MulticastSender:

    def __init__(self, port, mcgroup=None):
        if mcgroup is None:
            mcgroup = "239.255.255.250"
        if not isinstance(port, int) or not (0 < port < 65536):
            raise ValueError("port must be in 1..65535")
        self.port = port
        self.group = str(mcgroup)
        self._closed = False

        addr = ipaddress.ip_address(self.group)
        if addr.version == 4:
            self.family = socket.AF_INET
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            try:
                self.sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", 1))
                self.sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, struct.pack("b", 1))
            except OSError:
                pass
            self._dest = (self.group, self.port)
        else:
            self.family = socket.AF_INET6
            self.sock = socket.socket(
                socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            try:
                self.sock.setsockopt(socket.IPPROTO_IPV6,
                                     socket.IPV6_MULTICAST_HOPS, 1)
                self.sock.setsockopt(socket.IPPROTO_IPV6,
                                     socket.IPV6_MULTICAST_LOOP, 1)
            except OSError:
                pass
            self._dest = (self.group, self.port, 0, 0)

    def __call__(self, data):
        if self._closed:
            raise RuntimeError("MulticastSender is closed")
        if isinstance(data, str):
            payload = data.encode("utf-8")
        elif isinstance(data, (bytes, bytearray, memoryview)):
            payload = data
        else:
            payload = bytes(data)
        return self.sock.sendto(payload, self._dest)

    def close(self):
        if not self._closed:
            try:
                self.sock.close()
            finally:
                self._closed = True
