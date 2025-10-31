
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.dataset = rasterio.open(rfile, 'w', **rfile.profile)
        if overviews:
            if overviews_resampling is None:
                overviews_resampling = Resampling.nearest
            self.dataset.build_overviews(
                overviews, resampling=overviews_resampling, min_size=overviews_minsize)

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        window = rasterio.windows.Window(
            *key[1].start, key[1].stop - key[1].start, key[0].stop - key[0].start)
        self.dataset.write(item, window=window)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
