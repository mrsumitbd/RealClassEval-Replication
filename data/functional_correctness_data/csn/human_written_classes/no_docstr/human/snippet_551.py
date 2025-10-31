class MINIDUMP_MISC_INFO_2:
    size = 44

    def __init__(self):
        self.SizeOfInfo = None
        self.Flags1 = None
        self.ProcessId = None
        self.ProcessCreateTime = None
        self.ProcessUserTime = None
        self.ProcessKernelTime = None
        self.ProcessorMaxMhz = None
        self.ProcessorCurrentMhz = None
        self.ProcessorMhzLimit = None
        self.ProcessorMaxIdleState = None
        self.ProcessorCurrentIdleState = None

    @staticmethod
    def parse(buff):
        mmi = MINIDUMP_MISC_INFO_2()
        mmi.SizeOfInfo = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mmi.Flags1 = MinidumpMiscInfo2Flags1(int.from_bytes(buff.read(4), byteorder='little', signed=False))
        if mmi.Flags1 & MinidumpMiscInfo2Flags1.MINIDUMP_MISC1_PROCESS_ID:
            mmi.ProcessId = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        else:
            buff.read(4)
        if mmi.Flags1 & MinidumpMiscInfo2Flags1.MINIDUMP_MISC1_PROCESS_TIMES:
            mmi.ProcessCreateTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessUserTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessKernelTime = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        else:
            buff.read(12)
        if mmi.Flags1 & MinidumpMiscInfo2Flags1.MINIDUMP_MISC1_PROCESSOR_POWER_INFO:
            mmi.ProcessorMaxMhz = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessorCurrentMhz = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessorMhzLimit = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessorMaxIdleState = int.from_bytes(buff.read(4), byteorder='little', signed=False)
            mmi.ProcessorCurrentIdleState = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        else:
            buff.read(20)
        return mmi