class _StringBuffer:

    def __init__(self, value) -> None:
        self.bufstr = value
        self.bufpos = 0

    def read(self, n):
        pos = self.bufpos
        newpos = pos + n
        ret = self.bufstr[pos:newpos]
        self.bufpos = newpos
        return ret