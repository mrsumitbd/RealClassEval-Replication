
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = data_stream
        self.buffer = ''

    def read(self, size=None):
        if size is None:
            return ''.join(self.data_stream) + self.buffer
        while len(self.buffer) < size:
            try:
                self.buffer += next(self.data_stream)
            except StopIteration:
                break
        result = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return result
