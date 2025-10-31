import socket
from typing import Iterable, List, Tuple, Union
import threading


class DesignatedReceiversSender:

    def __init__(self, default_port: int, receivers: Iterable[Union[str, Tuple[str, int]]]):
        self._closed = False
        self._lock = threading.Lock()
        if not isinstance(default_port, int) or not (0 < default_port < 65536):
            raise ValueError(
                "default_port must be an integer between 1 and 65535")
        self._default_port = default_port

        normalized: List[Tuple[str, int]] = []
        for r in receivers or []:
            if isinstance(r, tuple):
                if len(r) != 2:
                    raise ValueError(
                        f"Receiver tuple must be (host, port), got: {r}")
                host, port = r
                if not isinstance(host, str) or not isinstance(port, int):
                    raise ValueError(
                        f"Receiver tuple must be (str, int), got: {r}")
                normalized.append((host, port))
            elif isinstance(r, str):
                s = r.strip()
                if not s:
                    continue
                # Try host:port for IPv4/hostname. IPv6 may contain colons, handle [addr]:port
                host = None
                port = None
                if s.startswith('['):
                    # [ipv6]:port
                    end = s.find(']')
                    if end == -1:
                        raise ValueError(f"Invalid receiver format: {r}")
                    host = s[1:end]
                    rest = s[end+1:].lstrip()
                    if rest.startswith(':'):
                        rest = rest[1:]
                        if not rest.isdigit():
                            raise ValueError(f"Invalid port in receiver: {r}")
                        port = int(rest)
                    else:
                        port = self._default_port
                else:
                    if ':' in s and s.count(':') == 1:
                        h, p = s.split(':', 1)
                        if p.isdigit():
                            host = h
                            port = int(p)
                        else:
                            host = s
                            port = self._default_port
                    else:
                        # Could be plain hostname or IPv6 without brackets; use default port
                        host = s
                        port = self._default_port
                normalized.append((host, port))
            else:
                raise TypeError(f"Unsupported receiver type: {type(r)}")

        if not normalized:
            raise ValueError("At least one receiver must be provided")

        # Resolve addresses
        # list of (family, sockaddr)
        self._targets: List[Tuple[int, Tuple]] = []
        for host, port in normalized:
            try:
                infos = socket.getaddrinfo(host, port, type=socket.SOCK_DGRAM)
            except socket.gaierror as e:
                raise ValueError(
                    f"Failed to resolve receiver {host}:{port} - {e}") from e
            # Prefer first result; include all unique sockaddrs to avoid duplicates across families
            seen = set()
            for family, socktype, proto, canonname, sockaddr in infos:
                if socktype != socket.SOCK_DGRAM:
                    continue
                key = (family, sockaddr)
                if key in seen:
                    continue
                seen.add(key)
                self._targets.append((family, sockaddr))

        if not self._targets:
            raise ValueError("No resolvable receiver addresses found")

        self._sockets = {}  # family -> socket
        # Create sockets lazily on first send to allow environments without certain families

    def __call__(self, data):
        if self._closed:
            raise RuntimeError("Sender is closed")
        if isinstance(data, str):
            payload = data.encode('utf-8')
        elif isinstance(data, (bytes, bytearray, memoryview)):
            payload = bytes(data)
        else:
            raise TypeError("data must be str or bytes-like")

        sent_count = 0
        with self._lock:
            for family, sockaddr in self._targets:
                sock = self._sockets.get(family)
                if sock is None:
                    try:
                        sock = socket.socket(family, socket.SOCK_DGRAM)
                        # For IPv6, try to allow dual-stack if supported (non-fatal if fails)
                        if family == socket.AF_INET6:
                            try:
                                sock.setsockopt(
                                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
                            except OSError:
                                pass
                        self._sockets[family] = sock
                    except OSError:
                        continue
                try:
                    sock.sendto(payload, sockaddr)
                    sent_count += 1
                except OSError:
                    continue
        return sent_count

    def close(self):
        '''Close the sender.'''
        if self._closed:
            return
        with self._lock:
            if self._closed:
                return
            for sock in self._sockets.values():
                try:
                    sock.close()
                except Exception:
                    pass
            self._sockets.clear()
            self._closed = True
