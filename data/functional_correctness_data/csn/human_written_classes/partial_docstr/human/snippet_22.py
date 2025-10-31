class Object:
    """Base class for all non-trivial data accessors."""
    __slots__ = ('_buf', '_byte_width')

    def __init__(self, buf, byte_width):
        self._buf = buf
        self._byte_width = byte_width

    @property
    def ByteWidth(self):
        return self._byte_width