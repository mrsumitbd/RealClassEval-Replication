
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = iter(data_stream)
        self.buffer = bytearray()

    def read(self, size=None):
        '''Read bytes from an iterator.'''
        if size is None:
            chunks = list(self.data_stream)
            result = bytes().join(chunks)
            self.buffer = bytearray()
            return result
        else:
            while len(self.buffer) < size:
                try:
                    chunk = next(self.data_stream)
                    self.buffer.extend(chunk)
                except StopIteration:
                    break
            result = bytes(self.buffer[:size])
            self.buffer = self.buffer[size:]
            return result
