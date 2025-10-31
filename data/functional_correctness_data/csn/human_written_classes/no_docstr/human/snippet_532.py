class CONTEXT:

    def __init__(self):
        self.P1Home = 0
        self.P2Home = 0
        self.P3Home = 0
        self.P4Home = 0
        self.P5Home = 0
        self.P6Home = 0
        self.ContextFlags = 0
        self.MxCsr = 0
        self.SegCs = 0
        self.SegDs = 0
        self.SegEs = 0
        self.SegFs = 0
        self.SegGs = 0
        self.SegSs = 0
        self.EFlags = 0
        self.Dr0 = 0
        self.Dr1 = 0
        self.Dr2 = 0
        self.Dr3 = 0
        self.Dr6 = 0
        self.Dr7 = 0
        self.Rax = 0
        self.Rcx = 0
        self.Rdx = 0
        self.Rbx = 0
        self.Rsp = 0
        self.Rbp = 0
        self.Rsi = 0
        self.Rdi = 0
        self.R8 = 0
        self.R9 = 0
        self.R10 = 0
        self.R11 = 0
        self.R12 = 0
        self.R13 = 0
        self.R14 = 0
        self.R15 = 0
        self.Rip = 0
        self.DUMMYUNIONNAME = None
        self.VectorRegister = []
        self.VectorControl = 0
        self.DebugControl = 0
        self.LastBranchToRip = 0
        self.LastBranchFromRip = 0
        self.LastExceptionToRip = 0
        self.LastExceptionFromRip = 0

    @classmethod
    def parse(cls, buff):
        ctx = cls()
        ctx.P1Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.P2Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.P3Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.P4Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.P5Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.P6Home = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.ContextFlags = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.MxCsr = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.SegCs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.SegDs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.SegEs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.SegFs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.SegGs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.SegSs = int.from_bytes(buff.read(2), byteorder='little', signed=False)
        ctx.EFlags = int.from_bytes(buff.read(4), byteorder='little', signed=False)
        ctx.Dr0 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Dr1 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Dr2 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Dr3 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Dr6 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Dr7 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rax = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rcx = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rdx = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rbx = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rsp = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rbp = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rsi = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rdi = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R8 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R9 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R10 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R11 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R12 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R13 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R14 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.R15 = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.Rip = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.DUMMYUNIONNAME = CTX_DUMMYUNIONNAME.parse(buff)
        ctx.VectorRegister = M128A.parse_array(buff, 26)
        ctx.VectorControl = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.DebugControl = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.LastBranchToRip = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.LastBranchFromRip = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.LastExceptionToRip = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        ctx.LastExceptionFromRip = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        return ctx

    def __str__(self):
        s = ''
        s += '%s: 0x%x (%d)\n' % ('P1Home', self.P1Home, self.P1Home)
        s += '%s: 0x%x (%d)\n' % ('P2Home', self.P2Home, self.P2Home)
        s += '%s: 0x%x (%d)\n' % ('P3Home', self.P3Home, self.P3Home)
        s += '%s: 0x%x (%d)\n' % ('P4Home', self.P4Home, self.P4Home)
        s += '%s: 0x%x (%d)\n' % ('P5Home', self.P5Home, self.P5Home)
        s += '%s: 0x%x (%d)\n' % ('P6Home', self.P6Home, self.P6Home)
        s += '%s: 0x%x (%d)\n' % ('ContextFlags', self.ContextFlags, self.ContextFlags)
        s += '%s: 0x%x (%d)\n' % ('MxCsr', self.MxCsr, self.MxCsr)
        s += '%s: 0x%x (%d)\n' % ('SegCs', self.SegCs, self.SegCs)
        s += '%s: 0x%x (%d)\n' % ('SegDs', self.SegDs, self.SegDs)
        s += '%s: 0x%x (%d)\n' % ('SegEs', self.SegEs, self.SegEs)
        s += '%s: 0x%x (%d)\n' % ('SegFs', self.SegFs, self.SegFs)
        s += '%s: 0x%x (%d)\n' % ('SegGs', self.SegGs, self.SegGs)
        s += '%s: 0x%x (%d)\n' % ('SegSs', self.SegSs, self.SegSs)
        s += '%s: 0x%x (%d)\n' % ('EFlags', self.EFlags, self.EFlags)
        s += '%s: 0x%x (%d)\n' % ('Dr0', self.Dr0, self.Dr0)
        s += '%s: 0x%x (%d)\n' % ('Dr1', self.Dr1, self.Dr1)
        s += '%s: 0x%x (%d)\n' % ('Dr2', self.Dr2, self.Dr2)
        s += '%s: 0x%x (%d)\n' % ('Dr3', self.Dr3, self.Dr3)
        s += '%s: 0x%x (%d)\n' % ('Dr6', self.Dr6, self.Dr6)
        s += '%s: 0x%x (%d)\n' % ('Dr7', self.Dr7, self.Dr7)
        s += '%s: 0x%x (%d)\n' % ('Rax', self.Rax, self.Rax)
        s += '%s: 0x%x (%d)\n' % ('Rcx', self.Rcx, self.Rcx)
        s += '%s: 0x%x (%d)\n' % ('Rdx', self.Rdx, self.Rdx)
        s += '%s: 0x%x (%d)\n' % ('Rbx', self.Rbx, self.Rbx)
        s += '%s: 0x%x (%d)\n' % ('Rsp', self.Rsp, self.Rsp)
        s += '%s: 0x%x (%d)\n' % ('Rbp', self.Rbp, self.Rbp)
        s += '%s: 0x%x (%d)\n' % ('Rsi', self.Rsi, self.Rsi)
        s += '%s: 0x%x (%d)\n' % ('Rdi', self.Rdi, self.Rdi)
        s += '%s: 0x%x (%d)\n' % ('R8', self.R8, self.R8)
        s += '%s: 0x%x (%d)\n' % ('R9', self.R9, self.R9)
        s += '%s: 0x%x (%d)\n' % ('R10', self.R10, self.R10)
        s += '%s: 0x%x (%d)\n' % ('R11', self.R11, self.R11)
        s += '%s: 0x%x (%d)\n' % ('R12', self.R12, self.R12)
        s += '%s: 0x%x (%d)\n' % ('R13', self.R13, self.R13)
        s += '%s: 0x%x (%d)\n' % ('R14', self.R14, self.R14)
        s += '%s: 0x%x (%d)\n' % ('R15', self.R15, self.R15)
        s += '%s: 0x%x (%d)\n' % ('Rip', self.Rip, self.Rip)
        s += '%s:' % 'DUMMYUNIONNAME'
        s += self.DUMMYUNIONNAME.__str__()
        return s