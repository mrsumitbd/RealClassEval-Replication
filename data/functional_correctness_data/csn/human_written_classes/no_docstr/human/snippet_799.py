class FileReader:

    def __init__(self, path, mode='r'):
        self.fd = open(path, mode)
        self.stderr = ''

    def readlines(self):
        for line in self.fd:
            yield line
        self.fd.close()