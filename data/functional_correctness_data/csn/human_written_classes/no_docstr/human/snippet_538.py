class XMM_SAVE_AREA32:

    def __init__(self):
        self.ControlWord = 0
        self.StatusWord = 0
        self.TagWord = 0
        self.Reserved1 = 0
        self.ErrorOpcode = 0
        self.ErrorOffset = 0
        self.ErrorSelector = 0
        self.Reserved2 = 0
        self.DataOffset = 0
        self.DataSelector = 0
        self.Reserved3 = 0
        self.MxCsr = 0
        self.MxCsr_Mask = 0
        self.FloatRegisters = []
        self.XmmRegisters = []
        self.Reserved4 = []

    @classmethod
    def parse(cls, buff):
        xmm = cls()
        xmm.ControlWord = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.StatusWord = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.TagWord = chr(int.from_bytes(buff.read(1), byteorder='little', signed=False))
        xmm.Reserved1 = chr(int.from_bytes(buff.read(1), byteorder='little', signed=False))
        xmm.ErrorOpcode = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.ErrorOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        xmm.ErrorSelector = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.Reserved2 = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.DataOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        xmm.DataSelector = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.Reserved3 = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        xmm.MxCsr = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        xmm.MxCsr_Mask = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        xmm.FloatRegisters = M128A.parse_array(buff, 8)
        xmm.XmmRegisters = M128A.parse_array(buff, 16)
        xmm.Reserved4 = [chr(int.from_bytes(buff.read(1), byteorder='little', signed=False)) for i in range(96)]
        return xmm

    def __str__(self):
        s = ''
        s += '%s: %x (%d)\n' % ('ControlWord', self.ControlWord, self.ControlWord)
        s += '%s: %x (%d)\n' % ('StatusWord', self.StatusWord, self.StatusWord)
        s += '%s: %s\n' % ('TagWord', self.TagWord)
        s += '%s: %s\n' % ('Reserved1', self.Reserved1)
        s += '%s: %x (%d)\n' % ('ErrorOpcode', self.ErrorOpcode, self.ErrorOpcode)
        s += '%s: %x (%d)\n' % ('ErrorOffset', self.ErrorOffset, self.ErrorOffset)
        s += '%s: %x (%d)\n' % ('ErrorSelector', self.ErrorSelector, self.ErrorSelector)
        s += '%s: %x (%d)\n' % ('Reserved2', self.Reserved2, self.Reserved2)
        s += '%s: %x (%d)\n' % ('DataOffset', self.DataOffset, self.DataOffset)
        s += '%s: %x (%d)\n' % ('DataSelector', self.DataSelector, self.DataSelector)
        s += '%s: %x (%d)\n' % ('Reserved3', self.Reserved3, self.Reserved3)
        s += '%s: %x (%d)\n' % ('MxCsr', self.MxCsr, self.MxCsr)
        s += '%s: %x (%d)\n' % ('MxCsr_Mask', self.MxCsr_Mask, self.MxCsr_Mask)
        s += '%s:\n' % 'FloatRegisters:'
        for freg in self.FloatRegisters:
            s += '\t%s' % freg
        s += '%s:\n' % 'XmmRegisters'
        for xreg in self.XmmRegisters:
            s += '\t%s' % xreg
        s += '%s: %s\n' % ('Reserved4', ''.join(self.Reserved4))
        return s