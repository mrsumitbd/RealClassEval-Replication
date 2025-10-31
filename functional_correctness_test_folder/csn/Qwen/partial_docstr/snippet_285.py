
import rasterio


class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.dataset = rasterio.open(rfile, 'r+')
        self.name = name

    def __setitem__(self, key, item):
        self.dataset.update_tags(self.name, **{key: item})

    def close(self):
        '''Close the file.'''
        self.dataset.close()
