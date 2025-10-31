class Line:

    def __init__(self, line_no, buffer, start, end):
        self.line_no = line_no
        self.start = start
        self.end = end
        self.buffer = buffer

    @property
    def content(self):
        return self.buffer[self.start:self.end]