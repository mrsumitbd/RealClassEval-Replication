class MINIDUMP_HANDLE_DATA_STREAM:

    def __init__(self):
        self.SizeOfHeader: int = None
        self.SizeOfDescriptor: int = None
        self.NumberOfDescriptors: int = None
        self.Reserved: int = None

    @staticmethod
    def parse(buff):
        mhds = MINIDUMP_HANDLE_DATA_STREAM()
        mhds.SizeOfHeader = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhds.SizeOfDescriptor = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhds.NumberOfDescriptors = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        mhds.Reserved = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return mhds