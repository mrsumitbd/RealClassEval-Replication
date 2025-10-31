class NameServer:
    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        import threading
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost

        self._running = threading.Event()
        self._thread = None
        self._sock = None
        self._lock = threading.Lock()
        self._address = None

    def _parse_address(self, nameserver_address):
        if nameserver_address is None:
            host = "127.0.0.1" if self.restrict_to_localhost else "0.0.0.0"
            port = 0
            return host, port
        if isinstance(nameserver_address, tuple) and len(nameserver_address) == 2:
            return nameserver_address[0], int(nameserver_address[1])
        if isinstance(nameserver_address, str):
            if ":" in nameserver_address:
                host, port = nameserver_address.rsplit(":", 1)
                return host, int(port)
            return nameserver_address, 0
        raise ValueError("Unsupported nameserver_address format")

    def _serve(self):
        import socket
        self._sock.settimeout(0.25)
        while self._running.is_set():
            try:
                # Accept and immediately close; just to keep the port alive.
                conn, _ = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            else:
                try:
                    conn.close()
                except Exception:
                    pass

    def run(self, address_receiver=None, nameserver_address=None):
        import socket
        with self._lock:
            if self._running.is_set():
                if callable(address_receiver):
                    try:
                        address_receiver(self._address)
                    except Exception:
                        pass
                return self._address

            host, port = self._parse_address(nameserver_address)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except Exception:
                pass
            sock.bind((host, port))
            sock.listen(5)
            bound_host, bound_port = sock.getsockname()
            self._sock = sock
            self._address = (bound_host, bound_port)
            self._running.set()

            if callable(address_receiver):
                # Notify in a separate thread to avoid blocking run.
                import threading

                def _notify():
                    try:
                        address_receiver(self._address)
                    except Exception:
                        pass

                threading.Thread(target=_notify, daemon=True).start()

            import threading
            self._thread = threading.Thread(target=self._serve, daemon=True)
            self._thread.start()

            return self._address

    def stop(self):
        with self._lock:
            if not self._running.is_set():
                return
            self._running.clear()
            try:
                if self._sock is not None:
                    try:
                        self._sock.shutdown(0)
                    except Exception:
                        pass
                    self._sock.close()
            finally:
                self._sock = None
        if self._thread is not None:
            try:
                self._thread.join(timeout=2.0)
            finally:
                self._thread = None
        self._address = None
