class MinidumpMemoryInfo:

    def __init__(self):
        self.BaseAddress = None
        self.AllocationBase = None
        self.AllocationProtect = None
        self.RegionSize = None
        self.State = None
        self.Protect = None
        self.Type = None

    @staticmethod
    def parse(t, buff):
        mmi = MinidumpMemoryInfo()
        mmi.BaseAddress = t.BaseAddress
        mmi.AllocationBase = t.AllocationBase
        mmi.AllocationProtect = t.AllocationProtect
        mmi.RegionSize = t.RegionSize
        mmi.State = t.State
        mmi.Protect = t.Protect
        mmi.Type = t.Type
        return mmi

    @staticmethod
    def get_header():
        t = ['BaseAddress', 'AllocationBase', 'AllocationProtect', 'RegionSize', 'State', 'Protect', 'Type']
        return t

    def to_row(self):
        t = [hex(self.BaseAddress), hex(self.AllocationBase), str(self.AllocationProtect), hex(self.RegionSize), self.State.name if self.State else 'N/A', self.Protect.name if self.Protect else 'N/A', self.Type.name if self.Type else 'N/A']
        return t