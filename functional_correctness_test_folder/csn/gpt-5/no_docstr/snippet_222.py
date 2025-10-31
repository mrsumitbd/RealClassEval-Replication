import time
import threading
import inspect


class Transport:
    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        if not callable(connect):
            raise TypeError(
                "connect must be a callable that establishes and returns a connection")
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
        if reconnect_timeout < 0:
            raise ValueError("reconnect_timeout must be >= 0")

        self._gateway = gateway
        self._connect_fn = connect
        self._timeout = float(timeout)
        self._reconnect_timeout = float(reconnect_timeout)
        self._connect_kwargs = dict(kwargs)

        self._lock = threading.RLock()
        self._conn = None
        self._closed = False

        # Attempt initial connection within timeout window
        self._establish(self._timeout)

    def _establish(self, timeout):
        deadline = time.monotonic() + timeout
        last_err = None
        while time.monotonic() < deadline and not self._closed:
            try:
                conn = self._call_connect(
                    self._connect_fn, self._gateway, deadline - time.monotonic())
                if conn is None:
                    raise RuntimeError("connect callable returned None")
                self._conn = conn
                return
            except Exception as e:
                last_err = e
                time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))
        if last_err:
            raise last_err
        raise TimeoutError("Connection establishment timed out")

    def _call_connect(self, fn, gateway, remaining_timeout):
        sig = inspect.signature(fn)
        kwargs = dict(self._connect_kwargs)
        bound = None
        try:
            bound = sig.bind_partial()
        except Exception:
            pass

        params = list(sig.parameters.values())
        args = []
        # Try to pass gateway if the function expects at least 1 positional argument
        if params and params[0].kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            args.append(gateway)
        else:
            kwargs.setdefault("gateway", gateway)

        # Try to pass timeout if acceptable
        if any(p.name == "timeout" for p in params) or "timeout" in kwargs or any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in params
        ):
            kwargs.setdefault("timeout", max(0.0, float(remaining_timeout)))

        return fn(*args, **kwargs)

    def _send_via(self, conn, message, remaining_timeout):
        # Try common send patterns
        # 1) conn.send(message, timeout=?)
        if hasattr(conn, "send") and callable(getattr(conn, "send")):
            send_fn = getattr(conn, "send")
            sig = None
            try:
                sig = inspect.signature(send_fn)
            except Exception:
                sig = None
            if sig:
                kwargs = {}
                if any(p.name == "timeout" for p in sig.parameters.values()) or any(
                    p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
                ):
                    kwargs["timeout"] = max(0.0, remaining_timeout)
                return send_fn(message, **kwargs)
            return send_fn(message)

        # 2) conn(message, timeout=?)
        if callable(conn):
            sig = None
            try:
                sig = inspect.signature(conn)
            except Exception:
                sig = None
            if sig:
                kwargs = {}
                if any(p.name == "timeout" for p in sig.parameters.values()) or any(
                    p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
                ):
                    kwargs["timeout"] = max(0.0, remaining_timeout)
                return conn(message, **kwargs)
            return conn(message)

        # 3) fallback to gateway if it has send
        if hasattr(self._gateway, "send") and callable(getattr(self._gateway, "send")):
            send_fn = getattr(self._gateway, "send")
            sig = None
            try:
                sig = inspect.signature(send_fn)
            except Exception:
                sig = None
            if sig:
                kwargs = {}
                if any(p.name == "timeout" for p in sig.parameters.values()) or any(
                    p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
                ):
                    kwargs["timeout"] = max(0.0, remaining_timeout)
                return send_fn(message, **kwargs)
            return send_fn(message)

        raise RuntimeError(
            "No valid send method available on connection or gateway")

    def disconnect(self):
        with self._lock:
            self._closed = True
            conn, self._conn = self._conn, None
        # Attempt graceful close outside lock
        if conn is not None:
            try:
                if hasattr(conn, "close") and callable(getattr(conn, "close")):
                    conn.close()
                elif hasattr(conn, "disconnect") and callable(getattr(conn, "disconnect")):
                    conn.disconnect()
            except Exception:
                pass

    def send(self, message):
        with self._lock:
            if self._closed:
                raise RuntimeError("Transport is closed")

            # Ensure connection, reconnect if needed
            if self._conn is None:
                self._establish(self._timeout)

            conn = self._conn

        # Try send, on failure attempt reconnect within reconnect_timeout and retry once
        start = time.monotonic()
        try:
            return self._send_via(conn, message, self._timeout)
        except Exception:
            # Try to reconnect within reconnect timeout
            with self._lock:
                # If already closed externally, abort
                if self._closed:
                    raise
                # Drop old connection
                old = self._conn
                self._conn = None
            if old is not None:
                try:
                    if hasattr(old, "close") and callable(getattr(old, "close")):
                        old.close()
                    elif hasattr(old, "disconnect") and callable(getattr(old, "disconnect")):
                        old.disconnect()
                except Exception:
                    pass

            remaining = max(0.0, self._reconnect_timeout -
                            (time.monotonic() - start))
            with self._lock:
                if not self._closed:
                    self._establish(remaining if remaining > 0 else 0.0)
                    conn2 = self._conn
                else:
                    raise RuntimeError("Transport is closed")

            return self._send_via(conn2, message, self._timeout)
