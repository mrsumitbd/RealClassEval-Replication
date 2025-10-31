
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.name = self.file.name

    def write(self, buf):
        '''Write `buf` to the file.'''
        self.file.write(buf)

    def close(self):
        '''Close the file.'''
        if not self.file.closed:
            self.file.close()

    def __del__(self):
        '''Ensure the file is closed and deleted when the object is destroyed.'''
        self.close()
        if os.path.exists(self.name):
            os.unlink(self.name)
