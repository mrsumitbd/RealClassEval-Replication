class Delimiter:

    def __init__(self, start, end, string):
        self.type = string[start:end]
        self.number = end - start
        self.active = True
        self.start = start
        self.end = end
        if self.type.startswith(('*', '_')):
            self.open = is_opener(start, end, string)
            self.close = is_closer(start, end, string)

    def remove(self, n, left=True):
        if self.number - n == 0:
            return False
        if left:
            self.start = self.start + n
            self.number = self.end - self.start
            self.type = self.type[n:]
            return True
        self.end = self.end - n
        self.number = self.end - self.start
        self.type = self.type[:n]
        return True

    def closed_by(self, other):
        if self.type[0] != other.type[0]:
            return False
        if self.open and self.close or (other.open and other.close):
            return (self.number + other.number) % 3 != 0 or (self.number % 3 == 0 and other.number % 3 == 0)
        return True

    def __repr__(self):
        if not self.type.startswith(('*', '_')):
            return '<Delimiter type={} active={}>'.format(repr(self.type), self.active)
        return '<Delimiter type={} active={} open={} close={}>'.format(repr(self.type), self.active, self.open, self.close)