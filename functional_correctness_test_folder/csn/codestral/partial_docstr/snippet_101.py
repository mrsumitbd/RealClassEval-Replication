
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self.file = tempfile.NamedTemporaryFile(mode='w+', delete=False)

    def write(self, buf):
        '''Write `buf` to the file.'''
        self.file.write(buf)

    def close(self):
        self.file.close()

    def __del__(self):
        self.file.close()
