class MinidumpHandleObjectInformation:

    def __init__(self):
        self.NextInfo = None
        self.InfoType: int = None
        self.SizeOfInfo: int = None
        self.info_bytes: bytes = None

    @staticmethod
    def parse(mhoi):
        t = MinidumpHandleObjectInformation()
        t.InfoType = mhoi.InfoType
        t.SizeOfInfo = mhoi.SizeOfInfo
        t.info_bytes = mhoi.info_bytes
        return t

    def __str__(self):
        return self.info_bytes.hex()