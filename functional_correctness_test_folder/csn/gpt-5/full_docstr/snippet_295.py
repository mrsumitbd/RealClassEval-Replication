import socket


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set settings.'''
        self._default_port = int(default_port)
        self._targets = []  # list of (family, sockaddr)
        self._sockets = {}  # family -> socket
        self._closed = False

        if receivers is None:
            receivers = []

        for r in receivers:
            for fam, sa in self._resolve_receiver(r):
                self._targets.append((fam, sa))

        # Create sockets per address family in use
        families = {fam for fam, _ in self._targets}
        for fam in families:
            s = socket.socket(fam, socket.SOCK_DGRAM)
            try:
                # Optional: allow sending without binding
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except OSError:
                pass
            self._sockets[fam] = s

    def __call__(self, data):
        '''Send messages from all receivers.'''
        if self._closed:
            raise RuntimeError("Sender is closed")

        if isinstance(data, str):
            payload = data.encode('utf-8')
        elif isinstance(data, (bytes, bytearray, memoryview)):
            payload = bytes(data)
        else:
            payload = bytes(data)

        for fam, addr in self._targets:
            sock = self._sockets.get(fam)
            if sock is None:
                # Create on demand if missing
                sock = socket.socket(fam, socket.SOCK_DGRAM)
                self._sockets[fam] = sock
            sock.sendto(payload, addr)

    def close(self):
        '''Close the sender.'''
        if self._closed:
            return
        for s in self._sockets.values():
            try:
                s.close()
            except Exception:
                pass
        self._sockets.clear()
        self._targets.clear()
        self._closed = True

    def _resolve_receiver(self, receiver):
        # Returns list of (family, sockaddr)
        host, port = None, None

        if isinstance(receiver, tuple):
            if len(receiver) == 2:
                host, port = receiver
            elif len(receiver) == 1:
                host = receiver[0]
                port = self._default_port
            else:
                # Possibly already a sockaddr tuple; try to detect by family later
                # We will attempt to use getaddrinfo if possible; else skip
                raise ValueError(f"Unsupported receiver tuple: {receiver}")
        elif isinstance(receiver, str):
            s = receiver.strip()
            if s.startswith('['):
                # [ipv6]:port or [ipv6]
                end = s.find(']')
                if end == -1:
                    raise ValueError(
                        f"Invalid IPv6 receiver string: {receiver}")
                host = s[1:end]
                rest = s[end+1:]
                if rest.startswith(':'):
                    port = rest[1:]
                else:
                    port = self._default_port
            else:
                # Determine if it's host:port (single colon) or raw host
                colon_count = s.count(':')
                if colon_count == 1:
                    host_part, port_part = s.split(':', 1)
                    host, port = host_part, port_part
                else:
                    # ambiguous IPv6 without brackets -> treat as host, default port
                    host, port = s, self._default_port
        else:
            raise ValueError(
                f"Unsupported receiver type: {type(receiver).__name__}")

        if port is None:
            port = self._default_port

        try:
            port = int(port)
        except (TypeError, ValueError):
            # allow service names
            pass

        results = []
        # Resolve using getaddrinfo for UDP
        for fam, socktype, proto, _, sockaddr in socket.getaddrinfo(
            host, port, family=socket.AF_UNSPEC, type=socket.SOCK_DGRAM
        ):
            if socktype != socket.SOCK_DGRAM:
                continue
            results.append((fam, sockaddr))

        # Deduplicate
        seen = set()
        deduped = []
        for fam, sa in results:
            key = (fam, sa)
            if key not in seen:
                seen.add(key)
                deduped.append((fam, sa))

        if not deduped:
            raise OSError(f"Could not resolve receiver {receiver}")

        return deduped
