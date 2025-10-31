
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
        self.dataset.write(item, key)

    def close(self):
        '''Close the file.'''
        self.dataset.close()

    def _build_overviews(self):
        levels = self._calculate_overview_levels()
        self.dataset.build_overviews(
            levels, resampling=self.overviews_resampling)

    def _calculate_overview_levels(self):
        levels = []
        size = max(self.dataset.width, self.dataset.height)
        while size > self.overviews_minsize:
            size = size // 2
            levels.append(size)
        return levels
