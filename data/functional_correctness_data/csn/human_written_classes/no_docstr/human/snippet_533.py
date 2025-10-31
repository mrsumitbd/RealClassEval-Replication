class CTX_DUMMYSTRUCTNAME:

    def __init__(self):
        self.Header = []
        self.Legacy = []
        self.Xmm0 = 0
        self.Xmm1 = 0
        self.Xmm2 = 0
        self.Xmm3 = 0
        self.Xmm4 = 0
        self.Xmm5 = 0
        self.Xmm6 = 0
        self.Xmm7 = 0
        self.Xmm8 = 0
        self.Xmm9 = 0
        self.Xmm10 = 0
        self.Xmm11 = 0
        self.Xmm12 = 0
        self.Xmm13 = 0
        self.Xmm14 = 0
        self.Xmm15 = 0

    @classmethod
    def parse(cls, buff):
        dsn = cls()
        dsn.Header = M128A.parse_array(buff, 2)
        dsn.Legacy = M128A.parse_array(buff, 8)
        dsn.Xmm0 = M128A.parse(buff)
        dsn.Xmm1 = M128A.parse(buff)
        dsn.Xmm2 = M128A.parse(buff)
        dsn.Xmm3 = M128A.parse(buff)
        dsn.Xmm4 = M128A.parse(buff)
        dsn.Xmm5 = M128A.parse(buff)
        dsn.Xmm6 = M128A.parse(buff)
        dsn.Xmm7 = M128A.parse(buff)
        dsn.Xmm8 = M128A.parse(buff)
        dsn.Xmm9 = M128A.parse(buff)
        dsn.Xmm10 = M128A.parse(buff)
        dsn.Xmm11 = M128A.parse(buff)
        dsn.Xmm12 = M128A.parse(buff)
        dsn.Xmm13 = M128A.parse(buff)
        dsn.Xmm14 = M128A.parse(buff)
        dsn.Xmm15 = M128A.parse(buff)
        return dsn

    def __str__(self):
        s = ''
        s += '%s:\n' % 'Header'
        for head in self.Header:
            s += '\t%s' % head
        s += '%s:\n' % 'Legacy'
        for leg in self.Legacy:
            s += '\t%s' % leg
        s += '%s: %s' % ('Xmm0', self.Xmm0)
        s += '%s: %s' % ('Xmm1', self.Xmm1)
        s += '%s: %s' % ('Xmm2', self.Xmm2)
        s += '%s: %s' % ('Xmm3', self.Xmm3)
        s += '%s: %s' % ('Xmm4', self.Xmm4)
        s += '%s: %s' % ('Xmm5', self.Xmm5)
        s += '%s: %s' % ('Xmm6', self.Xmm6)
        s += '%s: %s' % ('Xmm7', self.Xmm7)
        s += '%s: %s' % ('Xmm8', self.Xmm8)
        s += '%s: %s' % ('Xmm9', self.Xmm9)
        s += '%s: %s' % ('Xmm10', self.Xmm10)
        s += '%s: %s' % ('Xmm11', self.Xmm11)
        s += '%s: %s' % ('Xmm12', self.Xmm12)
        s += '%s: %s' % ('Xmm13', self.Xmm13)
        s += '%s: %s' % ('Xmm14', self.Xmm14)
        s += '%s: %s' % ('Xmm15', self.Xmm15)
        return s