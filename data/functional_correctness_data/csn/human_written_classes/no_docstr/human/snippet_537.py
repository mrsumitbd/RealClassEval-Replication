class WOW64_FLOATING_SAVE_AREA:

    def __init__(self):
        self.ControlWord = 0
        self.StatusWord = 0
        self.TagWord = 0
        self.ErrorOffset = 0
        self.ErrorSelector = 0
        self.DataOffset = 0
        self.DataSelector = 0
        self.RegisterArea = []
        self.Cr0NpxState = 0

    @classmethod
    def parse(cls, buff):
        ctx = cls()
        ctx.ControlWord = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.StatusWord = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.TagWord = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.ErrorOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.ErrorSelector = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.DataOffset = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.DataSelector = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.RegisterArea = int.from_bytes(buff.read(80), byteorder='little', signed=False)
        ctx.Cr0NpxState = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        return ctx

    def __str__(self):
        s = ''
        s += 'ControlWord: %x (%d)\n' % (self.ControlWord, self.ControlWord)
        s += 'StatusWord: %x (%d)\n' % (self.StatusWord, self.StatusWord)
        s += 'TagWord: %x (%d)\n' % (self.TagWord, self.TagWord)
        s += 'ErrorOffset: %x (%d)\n' % (self.ErrorOffset, self.ErrorOffset)
        s += 'ErrorSelector: %x (%d)\n' % (self.ErrorSelector, self.ErrorSelector)
        s += 'DataOffset: %x (%d)\n' % (self.DataOffset, self.DataOffset)
        s += 'DataSelector: %x (%d)\n' % (self.DataSelector, self.DataSelector)
        s += 'RegisterArea: %s\n' % str(self.RegisterArea)
        s += 'Cr0NpxState: %x (%d)' % (self.Cr0NpxState, self.Cr0NpxState)
        return s