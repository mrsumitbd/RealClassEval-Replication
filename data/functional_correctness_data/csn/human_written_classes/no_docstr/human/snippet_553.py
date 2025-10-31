from minidump.streams.MemoryListStream import MINIDUMP_MEMORY_DESCRIPTOR

class MINIDUMP_THREAD_EX:

    def __init__(self):
        self.ThreadId = None
        self.SuspendCount = None
        self.PriorityClass = None
        self.Priority = None
        self.Teb = None
        self.Stack = None
        self.ThreadContext = None
        self.BackingStore = None

    @staticmethod
    def parse(buff):
        mte = MINIDUMP_THREAD_EX()
        mte.ThreadId = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mte.SuspendCount = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mte.PriorityClass = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mte.Priority = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mte.Teb = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mte.Stack = MINIDUMP_MEMORY_DESCRIPTOR.parse(buff)
        mte.ThreadContext = MINIDUMP_LOCATION_DESCRIPTOR.parse(buff)
        mte.BackingStore = MINIDUMP_MEMORY_DESCRIPTOR.parse(buff)
        return mte

    @staticmethod
    def get_header():
        return ['ThreadId', 'SuspendCount', 'PriorityClass', 'Priority', 'Teb']

    def to_row(self):
        return [hex(self.ThreadId), str(self.SuspendCount), str(self.PriorityClass), str(self.Priority), hex(self.Teb)]