
import rasterio
from rasterio.enums import Resampling


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.rfile = rfile
        self.ds = rasterio.open(rfile, 'r+')
        self.closed = False

        if overviews is not None:
            if overviews_resampling is None:
                resampling = Resampling.nearest
            else:
                if isinstance(overviews_resampling, str):
                    resampling = getattr(Resampling, overviews_resampling)
                else:
                    resampling = overviews_resampling
            for bidx in self.ds.indexes:
                self.ds.build_overviews(
                    overviews, resampling=resampling, minsize=overviews_minsize)
            self.ds.update_tags(ns='rio_overview', resampling=resampling.name)

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        # key: (band, window) or window (all bands)
        if isinstance(key, tuple) and len(key) == 2:
            band, window = key
            self.ds.write(item, band, window=window)
        else:
            window = key
            self.ds.write(item, window=window)

    def close(self):
        '''Close the file.'''
        if not self.closed:
            self.ds.close()
            self.closed = True
