
import rasterio


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.rfile = rfile
        self.dataset = rasterio.open(rfile, 'r+')
        if overviews is not None:
            self.dataset.build_overviews(
                overviews, overviews_resampling, overviews_minsize)

    def __setitem__(self, key, item):
        self.dataset.write(item, key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
