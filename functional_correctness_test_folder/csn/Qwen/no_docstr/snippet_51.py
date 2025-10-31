
class Array:

    def __init__(self, fmt):
        self.fmt = fmt

    def __call__(self, buf):
        import struct
        return struct.unpack(self.fmt, buf)
