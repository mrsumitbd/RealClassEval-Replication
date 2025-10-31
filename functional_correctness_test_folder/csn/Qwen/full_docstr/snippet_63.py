
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = data_stream
        self.buffer = []

    def read(self, size=None):
        '''Read bytes from an iterator.'''
        if size is None:
            return b''.join(self.buffer) + b''.join(self.data_stream)

        while len(self.buffer) < size:
            try:
                self.buffer.append(next(self.data_stream))
            except StopIteration:
                break

        result = b''.join(self.buffer[:size])
        self.buffer = self.buffer[size:]
        return result
