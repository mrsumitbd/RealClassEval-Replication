class FileIterator:

    def __init__(self, path):
        self.input = open(path, 'rb')

    def __iter__(self):
        return self

    def __next__(self):
        buffer = self.input.read(1024)
        if buffer == b'':
            raise StopIteration
        return buffer