
class BufferWithSegmentsCollection:
    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, i):
        return self.segments[i]
