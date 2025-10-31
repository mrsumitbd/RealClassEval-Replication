
import h5py


class RIOTag:

    def __init__(self, rfile, name):
        self.rfile = h5py.File(rfile, 'a')
        self.group = self.rfile.create_group(name)

    def __setitem__(self, key, item):
        self.group.attrs[key] = item

    def close(self):
        self.rfile.close()
