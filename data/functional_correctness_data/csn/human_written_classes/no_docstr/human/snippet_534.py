class CTX_DUMMYUNIONNAME:

    def __init__(self):
        self.FltSave = []
        self.Q = []
        self.D = []
        self.DUMMYSTRUCTNAME = []
        self.S = []

    @classmethod
    def parse(cls, buff):
        dun = cls()
        dun.FltSave = XMM_SAVE_AREA32.parse(buff)
        dun.Q = NEON128.parse_array(buff, 16)
        dun.D = [int.from_bytes(buff.read(8), byteorder='little', signed=False) for i in range(32)]
        dun.DUMMYSTRUCTNAME = CTX_DUMMYSTRUCTNAME.parse(buff)
        dun.S = [int.from_bytes(buff.read(4), byteorder='little', signed=False) for i in range(32)]
        return dun

    def __str__(self):
        s = ''
        s += '%s: %s\n' % ('FltSave', self.FltSave)
        s += '%s:\n' % 'Q'
        for q in self.Q:
            s += '\t%s' % q.__str__()
        for d in self.D:
            s += '\t%d' % d
        s += '%s: %s' % ('DUMMYSTRUCTNAME', self.DUMMYSTRUCTNAME)
        s += '%s:\n' % 'S'
        for e in self.S:
            s += '\t%d' % e
        return s