
class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        self.rfile.update_tags(**{key: item})

    def close(self):
        '''Close the file.'''
        self.rfile.close()
