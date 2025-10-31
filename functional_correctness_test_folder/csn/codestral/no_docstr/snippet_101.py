
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.name = self.file.name

    def write(self, buf):
        self.file.write(buf.encode())

    def close(self):
        self.file.close()

    def __del__(self):
        self.file.close()
