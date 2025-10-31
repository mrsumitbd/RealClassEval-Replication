class MINIDUMP_UNLOADED_MODULE:

    def __init__(self):
        self.BaseOfImage = None
        self.SizeOfImage = None
        self.CheckSum = None
        self.TimeDateStamp = None
        self.ModuleNameRva = None

    def to_bytes(self):
        t = self.BaseOfImage.value.to_bytes(8, byteorder='little', signed=False)
        t += self.SizeOfImage.to_bytes(4, byteorder='little', signed=False)
        t += self.CheckSum.to_bytes(4, byteorder='little', signed=False)
        t += self.TimeDateStamp.to_bytes(4, byteorder='little', signed=False)
        t += self.ModuleNameRva.to_bytes(4, byteorder='little', signed=False)
        return t

    @staticmethod
    def parse(buff):
        mum = MINIDUMP_UNLOADED_MODULE()
        mum.BaseOfImage = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mum.SizeOfImage = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mum.CheckSum = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mum.TimeDateStamp = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mum.ModuleNameRva = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return mum