class MINIDUMP_MODULE_LIST:

    def __init__(self):
        self.NumberOfModules = None
        self.Modules = []

    def get_size(self):
        return 4 + len(self.Modules) * MINIDUMP_MODULE().get_size()

    def to_bytes(self):
        t = len(self.Modules).to_bytes(4, byteorder='little', signed=False)
        for module in self.Modules:
            t += module.to_bytes()
        return t

    @staticmethod
    def parse(buff):
        mml = MINIDUMP_MODULE_LIST()
        mml.NumberOfModules = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        for _ in range(mml.NumberOfModules):
            mml.Modules.append(MINIDUMP_MODULE.parse(buff))
        return mml