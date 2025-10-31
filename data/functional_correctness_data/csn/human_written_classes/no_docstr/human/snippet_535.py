class M128A:

    def __init__(self):
        self.Low = 0
        self.High = 0

    @classmethod
    def parse(cls, buff):
        m128a = cls()
        m128a.Low = int.from_bytes(buff.read(8), byteorder='little', signed=False)
        m128a.High = int.from_bytes(buff.read(8), byteorder='little', signed=True)
        return m128a

    @classmethod
    def parse_array(cls, buff, length):
        arr = []
        for i in range(length):
            arr.append(cls.parse(buff))
        return arr

    def __str__(self):
        s = ''
        s += 'Low: %x (%d)' % (self.Low, self.Low)
        s += 'High: %x (%d)\n' % (self.High, self.High)
        return s