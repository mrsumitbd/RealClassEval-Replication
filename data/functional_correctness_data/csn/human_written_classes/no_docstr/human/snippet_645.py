class NibWriter:

    def __init__(self, file):
        self.file = file

    def write(self, seq):
        assert False, 'NibWriter.write() is not implemented yet'

    def close(self):
        self.file.close()