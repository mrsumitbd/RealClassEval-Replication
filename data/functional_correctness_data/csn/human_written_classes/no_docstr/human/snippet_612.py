class BufferedStreamReader:
    BUFFER_SIZE = 1024

    def __init__(self, stream):
        self.stream = stream
        self.buffer = stream.read(self.BUFFER_SIZE)
        self.position = 0

    def read_char(self):
        if self._is_buffer_depleted():
            self._fill_buffer()
            if not self.buffer:
                return None
        char = self.buffer[self.position]
        self.position += 1
        return char

    def _is_buffer_depleted(self):
        return self.position >= len(self.buffer)

    def _fill_buffer(self):
        self.buffer = self.stream.read(self.BUFFER_SIZE)
        self.position = 0