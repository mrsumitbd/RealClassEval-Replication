class RIOTag:

    def __init__(self, rfile, name):
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        self.name = name
        self._owns_file = False
        if hasattr(rfile, "write") and hasattr(rfile, "flush"):
            self._fh = rfile
        else:
            self._fh = open(rfile, "a", encoding="utf-8")
            self._owns_file = True
        self._closed = False
        self._header_written = False
        self._write_header()

    def _write_header(self):
        if self._header_written:
            return
        self._fh.write(f"[RIOTag:{self.name}]\n")
        self._fh.flush()
        self._header_written = True

    def __setitem__(self, key, item):
        if self._closed:
            raise ValueError("RIOTag is closed")
        if not isinstance(key, str) or not key:
            raise ValueError("key must be a non-empty string")
        if "\n" in key:
            raise ValueError("key cannot contain newline characters")
        # Simple serialization
        try:
            import json
            value = json.dumps(item, ensure_ascii=False)
        except Exception:
            value = str(item)
        if "\n" in value:
            raise ValueError("value cannot contain newline characters")
        self._fh.write(f"{key} = {value}\n")
        self._fh.flush()

    def close(self):
        if self._closed:
            return
        self._fh.write(f"[/RIOTag:{self.name}]\n")
        self._fh.flush()
        if self._owns_file:
            try:
                self._fh.close()
            except Exception:
                pass
        self._closed = True
