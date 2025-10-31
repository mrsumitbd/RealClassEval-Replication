class MINIDUMP_THREAD_INFO_LIST:

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
        mtil = MINIDUMP_THREAD_INFO_LIST()
        mtil.SizeOfHeader = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mtil.SizeOfEntry = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mtil.NumberOfEntries = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return mtil