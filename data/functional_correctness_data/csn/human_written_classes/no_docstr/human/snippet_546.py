class MINIDUMP_MEMORY_INFO_LIST:

    def __init__(self):
        self.SizeOfHeader: int = 16
        self.SizeOfEntry: int = 48
        self.NumberOfEntries: int = None
        self.entries = []

    def get_size(self):
        return self.SizeOfHeader + len(self.entries) * MINIDUMP_MEMORY_INFO().get_size()

    def to_bytes(self):
        t = self.SizeOfHeader.to_bytes(4, byteorder='little', signed=False)
        t += self.SizeOfEntry.to_bytes(4, byteorder='little', signed=False)
        t += len(self.entries).to_bytes(8, byteorder='little', signed=False)
        return t

    @staticmethod
    def parse(buff):
        mhds = MINIDUMP_MEMORY_INFO_LIST()
        mhds.SizeOfHeader = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhds.SizeOfEntry = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhds.NumberOfEntries = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        return mhds