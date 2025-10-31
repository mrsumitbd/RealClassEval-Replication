
class NullFile:
    '''A file object that is associated to /dev/null.'''

    def __new__(cls):
        '''
        Pass through.
        '''
        instance = super().__new__(cls)
        instance._file = open('/dev/null', 'w+b')
        return instance

    def __init__(self):
        '''no-op'''
        pass

    def write(self, data):
        return self._file.write(data)

    def read(self, size=-1):
        return self._file.read(size)

    def readline(self, size=-1):
        return self._file.readline(size)

    def readlines(self, hint=-1):
        return self._file.readlines(hint)

    def writelines(self, lines):
        return self._file.writelines(lines)

    def flush(self):
        return self._file.flush()

    def seek(self, offset, whence=0):
        return self._file.seek(offset, whence)

    def tell(self):
        return self._file.tell()

    def close(self):
        return self._file.close()

    @property
    def closed(self):
        return self._file.closed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
