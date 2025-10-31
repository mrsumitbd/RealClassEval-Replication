class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        import threading
        import time
        self._time = time
        self._lock = threading.Lock()
        self._factory = gateway if callable(gateway) else None
        self._conn = None if callable(gateway) else gateway
        self._timeout = float(timeout) if timeout is not None else None
        self._reconnect_timeout = float(
            reconnect_timeout) if reconnect_timeout is not None else 0.0
        self._connect_kwargs = dict(kwargs) if kwargs else {}
        self._closed = False
        self._connected = False
        self._last_error = None

        if connect:
            self._connect()

    def _set_timeout(self, conn):
        if conn is None:
            return
        # Socket-like
        settimeout = getattr(conn, "settimeout", None)
        if callable(settimeout) and self._timeout is not None:
            try:
                settimeout(self._timeout)
                return
            except Exception:
                pass
        # Attribute-style
        if self._timeout is not None and hasattr(conn, "timeout"):
            try:
                setattr(conn, "timeout", self._timeout)
            except Exception:
                pass

    def _instantiate(self):
        if self._factory is None:
            return self._conn
        return self._factory(**self._connect_kwargs)

    def _connect_call(self, conn):
        connect = getattr(conn, "connect", None)
        if callable(connect):
            try:
                if self._connect_kwargs:
                    connect(**self._connect_kwargs)
                else:
                    connect()
            except TypeError:
                # Fallback to no-kwargs if signature mismatch
                connect()

    def _is_open(self, conn):
        if conn is None:
            return False
        # Try common indicators
        closed = getattr(conn, "closed", None)
        if isinstance(closed, bool):
            return not closed
        # Some transports expose is_connected or similar
        for attr in ("is_connected", "connected", "open"):
            val = getattr(conn, attr, None)
            if isinstance(val, bool):
                return bool(val)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
        # Otherwise assume it's open if we have an object and not explicitly closed
        return True

    def _connect(self):
        if self._closed:
            raise RuntimeError("Transport is closed")
        if self._connected and self._is_open(self._conn):
            return

        conn = self._conn
        if conn is None:
            conn = self._instantiate()

        self._set_timeout(conn)
        try:
            self._connect_call(conn)
        except Exception as e:
            self._last_error = e
            raise

        self._conn = conn
        self._connected = self._is_open(conn)

    def disconnect(self):
        '''Disconnect from the transport.'''
        with self._lock:
            conn = self._conn
            self._closed = True
            self._connected = False
            self._last_error = None
            self._conn = None
        # Perform close outside lock to avoid blocking other operations
        if conn is not None:
            # Try common close methods
            for method_name in ("disconnect", "close", "shutdown"):
                m = getattr(conn, method_name, None)
                if callable(m):
                    try:
                        # shutdown may require a how arg; try without
                        m()
                    except TypeError:
                        # For sockets: shutdown(2) is SHUT_RDWR; avoid importing socket
                        try:
                            m(2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                    break

    def _encode(self, message):
        if message is None:
            return b""
        if isinstance(message, (bytes, bytearray, memoryview)):
            b = bytes(message)
        elif isinstance(message, str):
            b = message.encode("utf-8")
        else:
            # Try to stringify
            b = str(message).encode("utf-8")
        return b

    def _write_once(self, conn, data):
        # Try common write/send methods. Return number of bytes sent or raise.
        if conn is None:
            raise RuntimeError("No connection available")

        # Prefer sendall if available (ensures full write)
        sendall = getattr(conn, "sendall", None)
        if callable(sendall):
            sendall(data)
            return len(data)

        # Fallback to send
        send = getattr(conn, "send", None)
        if callable(send):
            n = send(data)
            if n is None:
                # Some implementations return None on success for full length
                return len(data)
            return int(n)

        # File-like write
        write = getattr(conn, "write", None)
        if callable(write):
            n = write(data)
            if n is None:
                return len(data)
            return int(n)

        # Queue-like put
        put = getattr(conn, "put", None)
        if callable(put):
            put(data)
            return len(data)

        raise AttributeError(
            "Underlying gateway does not support sending/writing")

    def send(self, message):
        '''Write a message to the gateway.'''
        data = self._encode(message)
        deadline = self._time.monotonic() + max(self._reconnect_timeout, 0.0)
        attempt = 0
        last_exc = None

        while True:
            with self._lock:
                if not self._connected or not self._is_open(self._conn):
                    try:
                        self._connect()
                    except Exception as e:
                        last_exc = e
                        self._connected = False
                        self._conn = self._conn  # keep last for possible retries

                if self._connected and self._conn is not None:
                    try:
                        sent = self._write_once(self._conn, data)
                        return sent
                    except Exception as e:
                        last_exc = e
                        self._connected = False

            # Outside lock: backoff and retry until deadline
            attempt += 1
            now = self._time.monotonic()
            if now >= deadline:
                if last_exc:
                    raise last_exc
                raise TimeoutError("Failed to send before reconnect timeout")
            # simple backoff
            remaining = max(0.0, deadline - now)
            self._time.sleep(min(0.1 * attempt, 0.5, remaining))
