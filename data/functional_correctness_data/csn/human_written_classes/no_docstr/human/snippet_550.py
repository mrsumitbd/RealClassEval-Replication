class MINIDUMP_MISC_INFO:
    size = 24

    def __init__(self):
        self.SizeOfInfo = None
        self.Flags1 = None
        self.ProcessId = None
        self.ProcessCreateTime = None
        self.ProcessUserTime = None
        self.ProcessKernelTime = None

    @staticmethod
    def parse(buff):
        mmi = MINIDUMP_MISC_INFO()
        mmi.SizeOfInfo = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mmi.Flags1 = MinidumpMiscInfoFlags1(int.from_bytes(buff.read(4), byteorder='little', signed=False))
        if mmi.Flags1 & MinidumpMiscInfoFlags1.MINIDUMP_MISC1_PROCESS_ID:
            mmi.ProcessId = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        else:
            buff.read(4)
        if mmi.Flags1 & MinidumpMiscInfoFlags1.MINIDUMP_MISC1_PROCESS_TIMES:
            mmi.ProcessCreateTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessUserTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessKernelTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        else:
            buff.read(12)
        return mmi