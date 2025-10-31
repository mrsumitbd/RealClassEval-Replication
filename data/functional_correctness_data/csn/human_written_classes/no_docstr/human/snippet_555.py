class MINIDUMP_THREAD_INFO:

    def __init__(self):
        self.ThreadId = None
        self.DumpFlags = None
        self.DumpError = None
        self.ExitStatus = None
        self.CreateTime = None
        self.ExitTime = None
        self.KernelTime = None
        self.UserTime = None
        self.StartAddress = None
        self.Affinity = None

    def to_bytes(self):
        t = self.ThreadId.value.to_bytes(4, byteorder='little', signed=False)
        if self.DumpFlags:
            t += self.DumpFlags.value.to_bytes(4, byteorder='little', signed=False)
        else:
            t += b'\x00' * 4
        t += self.DumpError.to_bytes(4, byteorder='little', signed=False)
        t += self.ExitStatus.to_bytes(4, byteorder='little', signed=False)
        t += self.CreateTime.to_bytes(8, byteorder='little', signed=False)
        t += self.ExitTime.to_bytes(8, byteorder='little', signed=False)
        t += self.KernelTime.to_bytes(8, byteorder='little', signed=False)
        t += self.UserTime.to_bytes(8, byteorder='little', signed=False)
        t += self.StartAddress.to_bytes(8, byteorder='little', signed=False)
        t += self.Affinity.to_bytes(8, byteorder='little', signed=False)
        return t

    @staticmethod
    def parse(buff):
        mti = MINIDUMP_THREAD_INFO()
        mti.ThreadId = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        try:
            mti.DumpFlags = DumpFlags(int.from_bytes(buff.read(4), byteorder='little', signed=False))
        except:
            pass
        mti.DumpError = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mti.ExitStatus = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mti.CreateTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mti.ExitTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mti.KernelTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mti.UserTime = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mti.StartAddress = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mti.Affinity = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        return mti