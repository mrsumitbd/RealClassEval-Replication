class LoggerBackend:

    def __init__(self, **kwargs):
        import sys
        import threading

        self._lock = threading.RLock()
        self._owns_stream = False

        stream = kwargs.get("stream")
        filename = kwargs.get("filename")
        self._flush = bool(kwargs.get("flush", False))
        self._json = bool(kwargs.get("json", False))

        if stream is not None and filename is not None:
            raise ValueError(
                "Provide either 'stream' or 'filename', not both.")

        if filename is not None:
            self._stream = open(
                filename, "a", encoding=kwargs.get("encoding", "utf-8"))
            self._owns_stream = True
        elif stream is not None:
            if not hasattr(stream, "write"):
                raise TypeError(
                    "Provided 'stream' must be a file-like object with a 'write' method.")
            self._stream = stream
        else:
            self._stream = sys.stderr

        formatter = kwargs.get("formatter")
        if formatter is not None and not callable(formatter):
            raise TypeError("'formatter' must be callable.")
        self._formatter = formatter or self._default_format

    def _default_format(self, event):
        import datetime as _dt
        import json as _json

        ts = _dt.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

        if self._json:
            payload = event
            if not isinstance(event, dict):
                payload = {"message": str(event)}
            payload = {"timestamp": ts, **payload}
            try:
                return _json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
            except Exception:
                # Fallback to string if serialization fails
                return _json.dumps({"timestamp": ts, "message": str(event)}, ensure_ascii=False)
        else:
            if isinstance(event, dict):
                # Stable key order
                parts = []
                for k in sorted(event.keys(), key=lambda x: str(x)):
                    v = event[k]
                    try:
                        s = str(v)
                    except Exception:
                        s = repr(v)
                    parts.append(f"{k}={s}")
                body = " ".join(parts)
            elif isinstance(event, BaseException):
                body = f"{event.__class__.__name__}: {event}"
            else:
                body = str(event)
            return f"{ts} {body}"

    def send(self, event):
        line = self._formatter(event)
        if not line.endswith("\n"):
            line = line + "\n"
        with self._lock:
            self._stream.write(line)
            if self._flush:
                try:
                    self._stream.flush()
                except Exception:
                    pass

    def __del__(self):
        try:
            if self._owns_stream and self._stream:
                try:
                    self._stream.flush()
                except Exception:
                    pass
                try:
                    self._stream.close()
                except Exception:
                    pass
        except Exception:
            pass
