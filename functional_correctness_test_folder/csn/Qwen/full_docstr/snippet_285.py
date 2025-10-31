
import rasterio
from rasterio.profiles import DefaultGTiffProfile


class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name
        self.profile = DefaultGTiffProfile(count=1, dtype='float32')
        self.dataset = rasterio.open(self.rfile, 'w', **self.profile)

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        self.dataset.write(item, 1)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
