
import tempfile
import os


class ClosableNamedTemporaryFile:
    '''Creates a temporary file that is not deleted when the file is closed.
    This allows the file to be opened with an exclusive lock, but used by other programs before
    it is deleted
    '''

    def __init__(self):
        '''Create a temporary file.'''
        self.file = tempfile.NamedTemporaryFile(delete=False)

    def write(self, buf):
        '''Write `buf` to the file.'''
        self.file.write(buf)

    def close(self):
        '''Closes the file, allowing it to be opened by other programs. Does not delete the file.'''
        self.file.close()

    def __del__(self):
        '''Deletes the temporary file.'''
        try:
            os.unlink(self.file.name)
        except FileNotFoundError:
            pass
        except AttributeError:
            pass
