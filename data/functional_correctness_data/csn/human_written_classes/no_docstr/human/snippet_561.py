class POINTER:

    def __init__(self, reader, finaltype):
        self.location = reader.tell()
        self.value = reader.read_uint()
        self.finaltype = finaltype

    def read(self, reader, override_finaltype=None):
        if self.value == 0:
            return None
        pos = reader.tell()
        reader.move(self.value)
        if override_finaltype:
            data = override_finaltype(reader)
        else:
            data = self.finaltype(reader)
        reader.move(pos)
        return data

    def read_raw(self, reader, size):
        if self.value == 0:
            return None
        pos = reader.tell()
        reader.move(self.value)
        data = reader.read(size)
        reader.move(pos)
        return data