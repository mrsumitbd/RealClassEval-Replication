
import rasterio


class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.dataset = rasterio.open(rfile)
        self.tag = self.dataset.tags()
        self.name = name

    def __setitem__(self, key, item):
        self.tag[key] = item
        self.dataset.update_tags(**{self.name: self.tag})

    def close(self):
        '''Close the file.'''
        self.dataset.close()
