
class BufferWithSegmentsCollection:

    def __init__(self, segments):
        self.segments = segments

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, i):
        return self.segments[i]
