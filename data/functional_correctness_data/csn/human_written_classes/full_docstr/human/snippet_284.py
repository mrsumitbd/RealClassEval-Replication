from rasterio.enums import Resampling
from rasterio.windows import Window

class RIODataset:
    """A wrapper for a rasterio dataset."""

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        """Init the rasterio dataset."""
        self.rfile = rfile
        self.overviews = overviews
        if overviews_resampling is None:
            overviews_resampling = 'nearest'
        self.overviews_resampling = Resampling[overviews_resampling]
        self.overviews_minsize = overviews_minsize

    def __setitem__(self, key, item):
        """Put the data chunk in the image."""
        if len(key) == 3:
            indexes = list(range(key[0].start + 1, key[0].stop + 1, key[0].step or 1))
            y = key[1]
            x = key[2]
        else:
            indexes = 1
            y = key[0]
            x = key[1]
        chy_off = y.start
        chy = y.stop - y.start
        chx_off = x.start
        chx = x.stop - x.start
        self.rfile.write(item, window=Window(chx_off, chy_off, chx, chy), indexes=indexes)

    def close(self):
        """Close the file."""
        if self.overviews is not None:
            overviews = self.overviews
            if len(overviews) == 0:
                from rasterio.rio.overview import get_maximum_overview_level
                width = self.rfile.width
                height = self.rfile.height
                max_level = get_maximum_overview_level(width, height, self.overviews_minsize)
                overviews = [2 ** j for j in range(1, max_level + 1)]
            logger.debug('Building overviews %s with %s resampling', str(overviews), self.overviews_resampling.name)
            self.rfile.build_overviews(overviews, resampling=self.overviews_resampling)
        return self.rfile.close()