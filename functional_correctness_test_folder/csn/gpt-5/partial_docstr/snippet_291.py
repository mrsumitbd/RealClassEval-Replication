class SocketReceiver:

    def __init__(self):
        import threading
        self._sockets = set()
        self._lock = threading.Lock()

    def register(self, socket):
        '''Register the socket.'''
        with self._lock:
            self._sockets.add(socket)

    def unregister(self, socket):
        with self._lock:
            self._sockets.discard(socket)

    def receive(self, *sockets, timeout=None):
        import selectors

        if timeout is not None:
            if not isinstance(timeout, (int, float)) or timeout < 0:
                raise ValueError(
                    "timeout must be None or a non-negative number")

        with self._lock:
            registered = list(self._sockets)

        to_monitor = set(registered)
        for s in sockets:
            if s is None:
                continue
            to_monitor.add(s)

        if not to_monitor:
            # Nothing to wait on
            if timeout is not None and timeout > 0:
                # Simulate waiting with no sockets monitored
                import time
                time.sleep(timeout)
            return {}

        sel = selectors.DefaultSelector()
        try:
            for s in to_monitor:
                try:
                    sel.register(s, selectors.EVENT_READ)
                except Exception:
                    # Skip sockets that cannot be registered (e.g., closed)
                    pass

            events = sel.select(timeout)
            if not events:
                return {}

            results = {}
            for key, _ in events:
                sock = key.fileobj
                try:
                    # Read a chunk; do not block or loop indefinitely
                    # 64 KiB is a reasonable upper bound for a single read
                    data = sock.recv(65536)
                except BlockingIOError:
                    continue
                except Exception:
                    # On error, treat as closed
                    data = b""

                results[sock] = data

                if data == b"":
                    # Connection closed - if it's a registered socket, unregister it
                    with self._lock:
                        self._sockets.discard(sock)

            return results
        finally:
            try:
                sel.close()
            except Exception:
                pass
