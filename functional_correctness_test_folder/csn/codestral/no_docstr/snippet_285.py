
import pickle


class RIOTag:

    def __init__(self, rfile, name):
        self.rfile = rfile
        self.name = name
        self.data = {}

    def __setitem__(self, key, item):
        self.data[key] = item
        with open(self.rfile, 'wb') as f:
            pickle.dump(self.data, f)

    def close(self):
        with open(self.rfile, 'wb') as f:
            pickle.dump(self.data, f)
