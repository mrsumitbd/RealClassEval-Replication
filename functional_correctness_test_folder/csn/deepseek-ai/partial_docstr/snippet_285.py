
class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        if hasattr(self.rfile, 'tags'):
            self.rfile.tags().update({key: item})
        else:
            raise AttributeError("The file does not support tags.")

    def close(self):
        '''Close the file.'''
        if hasattr(self.rfile, 'close'):
            self.rfile.close()
        else:
            raise AttributeError("The file does not support closing.")
