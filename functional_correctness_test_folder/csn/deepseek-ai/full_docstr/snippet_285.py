
import rasterio


class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        with rasterio.open(self.rfile, 'r+') as dst:
            dst.update_tags(**{self.name: item})

    def close(self):
        '''Close the file.'''
        pass
