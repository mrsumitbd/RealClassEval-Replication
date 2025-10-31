class Array:

    def __init__(self, fmt):
        import struct
        if not isinstance(fmt, str) or not fmt:
            raise ValueError("fmt must be a non-empty struct format string")
        self._struct = struct.Struct(fmt)
        self._size = self._struct.size

    def __call__(self, buf):
        mv = memoryview(buf)
        if len(mv) % self._size != 0:
            raise ValueError(
                "Buffer size is not a multiple of the struct size")
        out = []
        unpack = self._struct.unpack
        size = self._size
        for i in range(0, len(mv), size):
            item = unpack(mv[i:i + size])
            if len(item) == 1:
                out.append(item[0])
            else:
                out.append(item)
        return out
