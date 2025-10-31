
class RIOTag:

    def __init__(self, rfile, name):
        self.rfile = rfile
        self.name = name
        self.data = {}

    def __setitem__(self, key, item):
        self.data[key] = item

    def close(self):
        self.rfile.close()
