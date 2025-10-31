
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.dataset = rasterio.open(rfile, 'r+')
        self.overviews = overviews
        self.overviews_resampling = overviews_resampling or Resampling.nearest
        self.overviews_minsize = overviews_minsize
        if self.overviews:
            self._build_overviews()

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        self.dataset.write(item, window=key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()

    def _build_overviews(self):
        '''Build overviews for the dataset.'''
        if self.dataset.width > self.overviews_minsize or self.dataset.height > self.overviews_minsize:
            self.dataset.build_overviews(
                self.overviews, resampling=self.overviews_resampling)
            self.dataset.update_tags(
                ns='rio_overview', resampling=str(self.overviews_resampling))
