
import rasterio


class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rasterio.open(rfile, 'r+')
        self.tag = self.rfile.tags(ns=name)

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        self.tag[key] = str(item)

    def close(self):
        '''Close the file.'''
        self.rfile.update_tags(ns=self.tag.namespace, **self.tag)
        self.rfile.close()
