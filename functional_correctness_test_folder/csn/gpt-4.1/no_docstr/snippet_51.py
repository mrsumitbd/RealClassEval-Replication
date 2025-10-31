
import struct


class Array:

    def __init__(self, fmt):
        self.fmt = fmt
        self.size = struct.calcsize(fmt)

    def __call__(self, buf):
        count = len(buf) // self.size
        return list(struct.iter_unpack(self.fmt, buf))
