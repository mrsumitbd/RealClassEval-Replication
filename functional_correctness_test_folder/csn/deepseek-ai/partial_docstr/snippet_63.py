
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = iter(data_stream)
        self.buffer = bytearray()

    def read(self, size=None):
        if size is None:
            chunks = []
            for chunk in self.data_stream:
                chunks.append(chunk)
            result = b''.join(chunks) + bytes(self.buffer)
            self.buffer.clear()
            return result
        else:
            while len(self.buffer) < size:
                try:
                    chunk = next(self.data_stream)
                    self.buffer.extend(chunk)
                except StopIteration:
                    break
            if len(self.buffer) <= size:
                result = bytes(self.buffer)
                self.buffer.clear()
                return result
            else:
                result = bytes(self.buffer[:size])
                self.buffer = self.buffer[size:]
                return result
