
import rasterio


class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name
        self.dataset = rasterio.open(rfile, 'r+')

    def __setitem__(self, key, item):
        tags = self.dataset.tags(ns=self.name)
        tags[key] = item
        self.dataset.update_tags(ns=self.name, **tags)

    def close(self):
        '''Close the file.'''
        if self.dataset:
            self.dataset.close()
            self.dataset = None
