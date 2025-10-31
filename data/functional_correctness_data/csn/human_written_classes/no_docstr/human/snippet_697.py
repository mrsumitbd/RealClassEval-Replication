import os

class DiskDictionary:

    def __init__(self, directory='.cache', funname='fun'):
        self.funname = funname
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.directory = directory

    def get_filename(self, key):
        import pickle
        hh = tuple((hashable(k) for k in key))
        h = hash(hh)
        filename = '{0}/{1}.{2}.pickle'.format(self.directory, self.funname, h)
        return filename

    def __setitem__(self, key, value):
        import pickle
        filename = self.get_filename(key)
        try:
            with open(filename, 'w') as f:
                pickle.dump(value, f)
        except TypeError as e:
            raise e

    def get(self, item):
        import pickle
        filename = self.get_filename(item)
        try:
            with open(filename) as f:
                value = pickle.load(f)
                return value
        except:
            return None