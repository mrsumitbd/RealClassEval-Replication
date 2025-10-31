
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.dataset = rasterio.open(rfile)
        if overviews is not None:
            self.dataset.build_overviews(
                overviews, Resampling[overviews_resampling] if overviews_resampling else Resampling.nearest)
            self.overviews = overviews
        else:
            self.overviews = None

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        self.dataset.write(item, *key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
