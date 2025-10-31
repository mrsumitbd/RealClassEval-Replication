
import struct


class Array:

    def __init__(self, fmt):
        self.fmt = fmt

    def __call__(self, buf):
        return struct.unpack(self.fmt, buf)
