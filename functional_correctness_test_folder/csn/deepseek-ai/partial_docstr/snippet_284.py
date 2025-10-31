
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.dataset = rasterio.open(rfile)
        self.overviews = overviews
        self.overviews_resampling = overviews_resampling or Resampling.nearest
        self.overviews_minsize = overviews_minsize

        if self.overviews is not None:
            self.dataset.build_overviews(
                self.overviews,
                resampling=self.overviews_resampling
            )

    def __setitem__(self, key, item):
        if isinstance(key, tuple) and len(key) == 2:
            self.dataset.write(item, key[0], window=key[1])
        else:
            self.dataset.write(item, key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()
