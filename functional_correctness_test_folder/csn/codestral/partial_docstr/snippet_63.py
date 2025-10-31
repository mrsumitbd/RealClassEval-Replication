
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = data_stream
        self.buffer = b''

    def read(self, size=None):
        if size is None:
            # Read all data from the stream
            data = self.buffer
            self.buffer = b''
            for chunk in self.data_stream:
                data += chunk
            return data
        else:
            # Read 'size' bytes from the stream
            data = self.buffer
            while len(data) < size:
                try:
                    chunk = next(self.data_stream)
                    data += chunk
                except StopIteration:
                    break
            self.buffer = data[size:]
            return data[:size]
