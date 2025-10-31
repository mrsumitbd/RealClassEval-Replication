
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.rfile = rfile
        self.ds = rasterio.open(rfile, 'r+')
        self._overviews = overviews
        self._overviews_resampling = overviews_resampling
        self._overviews_minsize = overviews_minsize

        if overviews is not None:
            for bidx in self.ds.indexes:
                factors = overviews
                self.ds.build_overviews(
                    factors, Resampling[overviews_resampling] if overviews_resampling else Resampling.nearest, band=bidx)
            self.ds.update_tags(ns='rio_overview',
                                resampling=overviews_resampling or 'nearest')
        elif overviews_minsize is not None:
            # Build overviews automatically until the smallest dimension is less than overviews_minsize
            for bidx in self.ds.indexes:
                width, height = self.ds.width, self.ds.height
                factors = []
                factor = 2
                while min(width // factor, height // factor) >= overviews_minsize:
                    factors.append(factor)
                    factor *= 2
                if factors:
                    self.ds.build_overviews(
                        factors, Resampling[overviews_resampling] if overviews_resampling else Resampling.nearest, band=bidx)
            self.ds.update_tags(ns='rio_overview',
                                resampling=overviews_resampling or 'nearest')

    def __setitem__(self, key, item):
        if isinstance(key, int):
            self.ds.write(item, key)
        elif isinstance(key, tuple):
            # key: (band, window)
            band, window = key
            self.ds.write(item, band, window=window)
        else:
            raise KeyError("Key must be an int (band) or tuple (band, window)")

    def close(self):
        '''Close the file.'''
        if self.ds:
            self.ds.close()
            self.ds = None
