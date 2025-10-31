class TimeOffset:
    """Temporarily applies specified offset (in microseconds) to time() function result."""

    def __init__(self, offset):
        self.offset = int(offset)

    def __enter__(self):
        global _offset_utime
        _offset_utime += self.offset

    def __exit__(self, typ, value, traceback):
        global _offset_utime
        _offset_utime -= self.offset