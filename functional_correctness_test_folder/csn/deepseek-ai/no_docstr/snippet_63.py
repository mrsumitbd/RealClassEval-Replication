
class StreamingFile:

    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.buffer = bytearray()

    def read(self, size=None):
        if size is None:
            # Read all remaining data
            chunk = self.data_stream.read()
            self.buffer.extend(chunk)
            result = bytes(self.buffer)
            self.buffer.clear()
            return result
        else:
            # Read until buffer has at least 'size' bytes or no more data
            while len(self.buffer) < size:
                chunk = self.data_stream.read(size - len(self.buffer))
                if not chunk:
                    break
                self.buffer.extend(chunk)
            if len(self.buffer) >= size:
                result = bytes(self.buffer[:size])
                self.buffer = self.buffer[size:]
            else:
                result = bytes(self.buffer)
                self.buffer.clear()
            return result
