
import rasterio
from rasterio.enums import Resampling


class RIODataset:

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        self.dataset = rasterio.open(rfile)
        self.overviews = overviews
        self.overviews_resampling = Resampling[overviews_resampling] if overviews_resampling else Resampling.nearest
        self.overviews_minsize = overviews_minsize

        if self.overviews is not None:
            self.dataset.build_overviews(
                self.overviews, resampling=self.overviews_resampling, min_size=self.overviews_minsize)
            self.dataset.update_tags(
                ns='rio_overview', resampling=self.overviews_resampling.name)

    def __setitem__(self, key, item):
        if isinstance(key, str):
            self.dataset.tags[key] = item
        else:
            raise TypeError("Key must be a string")

    def close(self):
        self.dataset.close()
