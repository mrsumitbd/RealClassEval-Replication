
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = iter(data_stream)
        self.buffer = b''

    def read(self, size=None):
        '''Read bytes from an iterator.'''
        if size is None:
            result = self.buffer
            self.buffer = b''
            for chunk in self.data_stream:
                result += chunk
            return result
        else:
            while len(self.buffer) < size:
                try:
                    chunk = next(self.data_stream)
                    self.buffer += chunk
                except StopIteration:
                    break
            result = self.buffer[:size]
            self.buffer = self.buffer[size:]
            return result
