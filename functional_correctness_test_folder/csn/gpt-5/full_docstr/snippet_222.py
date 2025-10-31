import time
import threading
import socket


class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        '''Set up transport.'''
        if not callable(connect):
            raise TypeError(
                "connect must be a callable that returns a connection object")
        self.gateway = gateway
        self._connect_func = connect
        self.timeout = float(timeout) if timeout is not None else None
        self.reconnect_timeout = float(
            reconnect_timeout) if reconnect_timeout is not None else 0.0
        self.kwargs = dict(kwargs) if kwargs else {}
        self._conn = None
        self._lock = threading.RLock()
        self._closed = False
        self._connect()

    def _set_timeout_if_possible(self, conn):
        if conn is None:
            return
        # socket-like
        try:
            if hasattr(conn, "settimeout"):
                conn.settimeout(self.timeout)
                return
        except Exception:
            pass
        # file-like: nothing generic to set

    def _connect(self):
        with self._lock:
            if self._closed:
                raise RuntimeError("Transport is closed")
            conn = self._connect_func(self.gateway, **self.kwargs)
            self._set_timeout_if_possible(conn)
            self._conn = conn

    def _close_conn(self, conn):
        try:
            if conn is None:
                return
            if hasattr(conn, "close"):
                conn.close()
        except Exception:
            pass

    def disconnect(self):
        '''Disconnect from the transport.'''
        with self._lock:
            self._closed = True
            conn, self._conn = self._conn, None
        self._close_conn(conn)

    def _ensure_connected(self, start_time=None):
        with self._lock:
            if self._closed:
                raise RuntimeError("Transport is closed")
            if self._conn is not None:
                return
        # attempt reconnects outside lock to avoid blocking other operations
        deadline = None if self.reconnect_timeout is None else (
            (start_time or time.monotonic()) + float(self.reconnect_timeout)
        )
        delay = 0.05
        while True:
            try:
                self._connect()
                return
            except Exception:
                if deadline is not None and time.monotonic() >= deadline:
                    raise
                time.sleep(delay)
                delay = min(delay * 2, 1.0)

    def _send_bytes(self, data):
        conn = self._conn
        if conn is None:
            raise ConnectionError("Not connected")
        # Preferred order: sendall, send, write(+flush)
        if hasattr(conn, "sendall"):
            conn.sendall(data)
            return
        if hasattr(conn, "send"):
            total = 0
            n = len(data)
            while total < n:
                sent = conn.send(data[total:])
                if sent is None:
                    raise RuntimeError("send returned None")
                if sent == 0:
                    raise ConnectionError("Socket connection broken")
                total += sent
            return
        if hasattr(conn, "write"):
            written = conn.write(data)
            if hasattr(conn, "flush"):
                try:
                    conn.flush()
                except Exception:
                    pass
            if written is not None and written != len(data):
                raise IOError("Short write")
            return
        raise TypeError("Connection object does not support sending data")

    def send(self, message):
        '''Write a message to the gateway.'''
        if message is None:
            raise ValueError("message cannot be None")
        if isinstance(message, str):
            data = message.encode("utf-8")
        elif isinstance(message, (bytes, bytearray, memoryview)):
            data = bytes(message)
        else:
            data = str(message).encode("utf-8")

        with self._lock:
            if self._closed:
                raise RuntimeError("Transport is closed")

        start = time.monotonic()
        try:
            self._ensure_connected(start_time=start)
            with self._lock:
                self._send_bytes(data)
            return

        except Exception:
            # Attempt reconnect loop and retry send
            deadline = start + float(self.reconnect_timeout)
            last_err = None
            delay = 0.05
            while time.monotonic() < deadline:
                try:
                    # Close old conn (if any) and reconnect
                    old = None
                    with self._lock:
                        old, self._conn = self._conn, None
                    self._close_conn(old)
                    self._ensure_connected(start_time=start)
                    with self._lock:
                        self._send_bytes(data)
                    return
                except Exception as e:
                    last_err = e
                    time.sleep(delay)
                    delay = min(delay * 2, 1.0)
            if last_err:
                raise last_err
            raise ConnectionError(
                "Failed to send message within reconnect timeout")
