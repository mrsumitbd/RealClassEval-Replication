class VirtualSegment:

    def __init__(self, start, end, start_file_address):
        self.start = start
        self.end = end
        self.start_file_address = start_file_address
        self.data = None

    def inrange(self, start, end):
        return self.start <= start and end <= self.end