import struct

class UnpackWrapper:

    def __init__(self, file):
        self.file = file

    def read(self, amt):
        return self.file.read(amt)

    def get(self, fmt):
        t = struct.unpack(fmt, self.file.read(struct.calcsize(fmt)))
        return t[0]