
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')

    def write(self, buf):
        '''Write `buf` to the file.'''
        self.temp_file.write(buf)

    def close(self):
        self.temp_file.close()
        os.remove(self.temp_file.name)

    def __del__(self):
        if not self.temp_file.closed:
            self.close()
