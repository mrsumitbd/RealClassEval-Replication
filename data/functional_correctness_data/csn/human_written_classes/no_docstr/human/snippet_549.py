class MINIDUMP_MEMORY_LIST:

    def __init__(self):
        self.NumberOfMemoryRanges = None
        self.MemoryRanges = []

    def to_bytes(self):
        t = len(self.MemoryRanges).to_bytes(4, byteorder='little', signed=False)
        for memrange in self.MemoryRanges:
            t += memrange.to_bytes()
        return t

    @staticmethod
    def parse(buff):
        mml = MINIDUMP_MEMORY_LIST()
        mml.NumberOfMemoryRanges = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        for _ in range(mml.NumberOfMemoryRanges):
            mml.MemoryRanges.append(MINIDUMP_MEMORY_DESCRIPTOR.parse(buff))
        return mml

    def __str__(self):
        t = '== MINIDUMP_MEMORY_LIST ==\n'
        t += 'NumberOfMemoryRanges: %s\n' % self.NumberOfMemoryRanges
        for range in self.MemoryRanges:
            t += str(range)
        return t