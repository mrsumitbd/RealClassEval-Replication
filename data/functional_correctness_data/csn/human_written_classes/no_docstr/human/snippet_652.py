class MultiPartIO:

    def __init__(self, body, callback=None):
        self.to_read = body
        self.have_read = []
        self._total = 0
        self.callback = callback
        self.cursor = None

    def read(self, n=-1):
        if self.callback:
            self.callback(self.tell(), self._total)
        if n == -1:
            return b''.join((fd.read() for fd in self.to_read))
        if not self.to_read:
            return b''
        while self.to_read:
            data = self.to_read[0].read(n)
            if data:
                return data
            file_obj = self.to_read.pop(0)
            self.have_read.append(file_obj)
        return b''

    def tell(self):
        cursor = sum((fd.tell() for fd in self.have_read))
        if self.to_read:
            cursor += self.to_read[0].tell()
        return cursor

    def seek(self, pos, mode=0):
        assert pos == 0
        if mode == 0:
            self.to_read = self.have_read + self.to_read
            self.have_read = []
            for fd in self.to_read:
                fd.seek(pos, mode)
            self.cursor = 0
        elif mode == 2:
            self.have_read = self.have_read + self.to_read
            self.to_read = []
            for fd in self.have_read:
                fd.seek(pos, mode)
            self._total = self.tell()