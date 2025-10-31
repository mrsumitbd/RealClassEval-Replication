
import rasterio


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.rfile = rfile
        self.dataset = rasterio.open(
            rfile, 'r+', overviews=overviews, resampling=overviews_resampling, minsize=overviews_minsize)

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        self.dataset.write(item, key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
