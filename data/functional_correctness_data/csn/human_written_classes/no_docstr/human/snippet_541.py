class MINIDUMP_HANDLE_DESCRIPTOR:
    size = 32

    def __init__(self):
        self.Handle: int = None
        self.TypeNameRva: int = None
        self.ObjectNameRva: int = None
        self.Attributes: int = None
        self.GrantedAccess: int = None
        self.HandleCount: int = None
        self.PointerCount: int = None

    @staticmethod
    def parse(buff):
        mhd = MINIDUMP_HANDLE_DESCRIPTOR()
        mhd.Handle = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        mhd.TypeNameRva = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhd.ObjectNameRva = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhd.Attributes = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhd.GrantedAccess = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhd.HandleCount = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhd.PointerCount = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return mhd