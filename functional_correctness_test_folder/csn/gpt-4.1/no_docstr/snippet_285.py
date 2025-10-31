
class RIOTag:

    def __init__(self, rfile, name):
        self.rfile = rfile
        self.name = name
        self.closed = False
        self.data = {}

    def __setitem__(self, key, item):
        if self.closed:
            raise ValueError("Cannot set item on closed RIOTag")
        self.data[key] = item

    def close(self):
        self.closed = True
