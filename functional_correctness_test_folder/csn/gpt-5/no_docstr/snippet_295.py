import socket
from typing import Iterable, Tuple, Union, List, Dict, Any


class DesignatedReceiversSender:

    def __init__(self, default_port: int, receivers: Iterable[Union[str, Tuple[str, int], Tuple[str]]]):
        if not isinstance(default_port, int) or not (0 <= default_port <= 65535):
            raise ValueError(
                "default_port must be an integer between 0 and 65535")
        self._default_port = default_port

        self._targets: List[Tuple[int, int, int, Any]] = []
        self._sockets: Dict[Tuple[int, int, int], socket.socket] = {}
        self._closed = False

        parsed = [self._parse_receiver(r) for r in receivers]
        if not parsed:
            raise ValueError("receivers cannot be empty")

        for host, port in parsed:
            for fam, stype, proto, _, sockaddr in socket.getaddrinfo(host, port, 0, socket.SOCK_DGRAM, 0, socket.AI_ADDRCONFIG):
                self._targets.append((fam, stype, proto, sockaddr))

        if not self._targets:
            raise ValueError("No valid receiver addresses resolved")

        for fam, stype, proto, _ in self._targets:
            key = (fam, stype, proto)
            if key not in self._sockets:
                s = socket.socket(fam, stype, proto)
                # Allow IPv6 socket to send IPv4-mapped if possible
                if fam == socket.AF_INET6:
                    try:
                        s.setsockopt(socket.IPPROTO_IPV6,
                                     socket.IPV6_V6ONLY, 0)
                    except OSError:
                        pass
                s.setblocking(True)
                self._sockets[key] = s

    def __call__(self, data: Union[bytes, bytearray, memoryview, str]) -> int:
        if self._closed:
            raise RuntimeError("Sender is closed")
        if isinstance(data, str):
            payload = data.encode("utf-8")
        elif isinstance(data, (bytes, bytearray, memoryview)):
            payload = bytes(data)
        else:
            raise TypeError("data must be bytes-like or str")

        sent_count = 0
        for fam, stype, proto, sockaddr in self._targets:
            sock = self._sockets.get((fam, stype, proto))
            if sock is None:
                continue
            try:
                sock.sendto(payload, sockaddr)
                sent_count += 1
            except OSError:
                # Continue sending to other receivers
                continue
        return sent_count

    def close(self):
        if self._closed:
            return
        self._closed = True
        for s in self._sockets.values():
            try:
                s.close()
            except Exception:
                pass
        self._sockets.clear()
        self._targets.clear()

    def _parse_receiver(self, r: Union[str, Tuple[str, int], Tuple[str]]) -> Tuple[str, int]:
        if isinstance(r, tuple):
            if len(r) == 2:
                host, port = r
                if port is None:
                    port = self._default_port
            elif len(r) == 1:
                host = r[0]
                port = self._default_port
            else:
                raise ValueError(f"Invalid receiver tuple: {r}")
            return self._validate_host_port(host, port)

        if isinstance(r, str):
            r = r.strip()
            if not r:
                raise ValueError("Empty receiver string")
            if r.startswith("["):
                # Bracketed IPv6: [addr]:port or [addr]
                end = r.find("]")
                if end == -1:
                    raise ValueError(f"Invalid bracketed address: {r}")
                host = r[1:end]
                rest = r[end + 1:]
                if rest.startswith(":"):
                    port_str = rest[1:]
                    port = int(port_str)
                else:
                    port = self._default_port
            else:
                if ":" in r:
                    host_part, port_part = r.rsplit(":", 1)
                    host = host_part
                    port = int(port_part)
                else:
                    host = r
                    port = self._default_port
            return self._validate_host_port(host, port)

        raise TypeError(f"Unsupported receiver type: {type(r)}")

    def _validate_host_port(self, host: Any, port: Any) -> Tuple[str, int]:
        if not isinstance(host, str) or not host:
            raise ValueError(f"Invalid host: {host!r}")
        if not isinstance(port, int) or not (0 <= port <= 65535):
            raise ValueError(f"Invalid port: {port!r}")
        return host, port
