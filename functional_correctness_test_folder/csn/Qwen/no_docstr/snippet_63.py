
class StreamingFile:

    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.position = 0

    def read(self, size=None):
        if size is None:
            data = self.data_stream[self.position:]
            self.position = len(self.data_stream)
        else:
            data = self.data_stream[self.position:self.position + size]
            self.position += size
        return data
