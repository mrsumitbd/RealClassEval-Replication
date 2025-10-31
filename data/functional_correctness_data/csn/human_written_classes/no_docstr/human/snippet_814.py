class NonceParse:

    def __init__(self, bytes):
        self.bytes = bytes

    @property
    def type(self):
        return '.'.join((str(e) for e in list(self.bytes.contents[2:11])))

    @property
    def critical(self):
        return self.bytes.contents[13] == 255

    @property
    def value(self):
        return self.bytes[16:]