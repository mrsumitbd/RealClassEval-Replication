class MINIDUMP_UNLOADED_MODULE_LIST:

    def __init__(self):
        self.SizeOfHeader = None
        self.SizeOfEntry = None
        self.NumberOfEntries = None

    def to_bytes(self):
        t = self.SizeOfHeader.value.to_bytes(4, byteorder='little', signed=False)
        t += self.SizeOfEntry.to_bytes(4, byteorder='little', signed=False)
        t += self.NumberOfEntries.to_bytes(4, byteorder='little', signed=False)
        return t

    @staticmethod
    def parse(buff):
        muml = MINIDUMP_UNLOADED_MODULE_LIST()
        muml.SizeOfHeader = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        muml.SizeOfEntry = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        muml.NumberOfEntries = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return muml