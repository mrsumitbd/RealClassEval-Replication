class WOW64_CONTEXT:

    def __init__(self):
        self.ContextFlags = 0
        self.Dr0 = 0
        self.Dr1 = 0
        self.Dr2 = 0
        self.Dr3 = 0
        self.Dr6 = 0
        self.Dr7 = 0
        self.FloatSave = 0
        self.SegGs = 0
        self.SegFs = 0
        self.SegEs = 0
        self.SegDs = 0
        self.Edi = 0
        self.Esi = 0
        self.Ebx = 0
        self.Edx = 0
        self.Ecx = 0
        self.Eax = 0
        self.Ebp = 0
        self.Eip = 0
        self.SegCs = 0
        self.EFlags = 0
        self.Esp = 0
        self.SegSs = 0
        self.ExtendedRegisters = []

    @classmethod
    def parse(cls, buff):
        ctx = cls()
        ctx.ContextFlags = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr0 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr1 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr2 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr3 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr6 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr7 = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.FloatSave = WOW64_FLOATING_SAVE_AREA.parse(buff)
        ctx.SegGs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegFs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegEs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegDs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Edi = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Esi = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Ebx = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Edx = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Ecx = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Eax = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Ebp = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Eip = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegCs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.EFlags = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Esp = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegSs = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.ExtendedRegisters = [int.from_bytes(buff.read(1), byteorder='little', signed=False) for i in range(512)]
        return ctx

    def __str__(self):
        s = ''
        s += '%s: %x (%d)\n' % ('ContextFlags', self.ContextFlags, self.ContextFlags)
        s += '%s: %x (%d)\n' % ('Dr0', self.Dr0, self.Dr0)
        s += '%s: %x (%d)\n' % ('Dr1', self.Dr1, self.Dr1)
        s += '%s: %x (%d)\n' % ('Dr2', self.Dr2, self.Dr2)
        s += '%s: %x (%d)\n' % ('Dr3', self.Dr3, self.Dr3)
        s += '%s: %x (%d)\n' % ('Dr6', self.Dr6, self.Dr6)
        s += '%s: %x (%d)\n' % ('Dr7', self.Dr7, self.Dr7)
        s += '%s: %s\n' % ('FloatSave', self.FloatSave.__str__())
        s += '%s: %x (%d)\n' % ('SegGs', self.SegGs, self.SegGs)
        s += '%s: %x (%d)\n' % ('SegFs', self.SegFs, self.SegFs)
        s += '%s: %x (%d)\n' % ('SegEs', self.SegEs, self.SegEs)
        s += '%s: %x (%d)\n' % ('SegDs', self.SegDs, self.SegDs)
        s += '%s: %x (%d)\n' % ('Edi', self.Edi, self.Edi)
        s += '%s: %x (%d)\n' % ('Esi', self.Esi, self.Esi)
        s += '%s: %x (%d)\n' % ('Ebx', self.Ebx, self.Ebx)
        s += '%s: %x (%d)\n' % ('Edx', self.Edx, self.Edx)
        s += '%s: %x (%d)\n' % ('Ecx', self.Ecx, self.Ecx)
        s += '%s: %x (%d)\n' % ('Eax', self.Eax, self.Eax)
        s += '%s: %x (%d)\n' % ('Ebp', self.Ebp, self.Ebp)
        s += '%s: %x (%d)\n' % ('Eip', self.Eip, self.Eip)
        s += '%s: %x (%d)\n' % ('SegCs', self.SegCs, self.SegCs)
        s += '%s: %x (%d)\n' % ('EFlags', self.EFlags, self.EFlags)
        s += '%s: %x (%d)\n' % ('Esp', self.Esp, self.Esp)
        s += '%s: %x (%d)\n' % ('SegSs', self.SegSs, self.SegSs)
        s += '%s: %s\n' % ('ExtendedRegisters', str(self.ExtendedRegisters))
        return s