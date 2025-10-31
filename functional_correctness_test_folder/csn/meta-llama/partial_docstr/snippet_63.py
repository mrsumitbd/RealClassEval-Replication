
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self.data_stream = iter(data_stream)
        self.buffer = b''

    def read(self, size=None):
        '''Read data from the stream.

        Args:
            size (int, optional): The number of bytes to read. If None, read until the end of the stream.

        Returns:
            bytes: The data read from the stream.
        '''
        if size is None:
            # Read until the end of the stream
            result = self.buffer
            self.buffer = b''
            for chunk in self.data_stream:
                result += chunk
            return result
        else:
            # Read 'size' bytes from the stream
            result = b''
            while len(result) < size:
                if self.buffer:
                    chunk = self.buffer[:size - len(result)]
                    self.buffer = self.buffer[size - len(result):]
                    result += chunk
                else:
                    try:
                        self.buffer = next(self.data_stream)
                    except StopIteration:
                        break
            return result
