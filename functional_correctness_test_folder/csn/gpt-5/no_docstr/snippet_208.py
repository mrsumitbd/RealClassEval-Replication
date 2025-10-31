class NullFile:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            obj = super().__new__(cls)
            obj._closed = False
            cls._instance = obj
        return cls._instance

    def __init__(self):
        pass

    def write(self, s):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return 0 if s is None else len(s)

    def writelines(self, lines):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        for _ in lines:
            pass

    def read(self, size=-1):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return ""

    def readline(self, size=-1):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return ""

    def readlines(self, hint=-1):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return []

    def flush(self):
        if self._closed:
            raise ValueError("I/O operation on closed file.")

    def close(self):
        self._closed = True

    @property
    def closed(self):
        return self._closed

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False

    def fileno(self):
        raise OSError("NullFile has no file descriptor.")

    def __enter__(self):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False
