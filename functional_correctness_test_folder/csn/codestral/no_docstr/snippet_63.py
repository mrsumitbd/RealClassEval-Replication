
class StreamingFile:

    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.buffer = b''

    def read(self, size=None):
        if size is None:
            data = self.buffer + self.data_stream.read()
            self.buffer = b''
            return data
        else:
            while len(self.buffer) < size:
                chunk = self.data_stream.read(size - len(self.buffer))
                if not chunk:
                    break
                self.buffer += chunk
            data = self.buffer[:size]
            self.buffer = self.buffer[size:]
            return data
