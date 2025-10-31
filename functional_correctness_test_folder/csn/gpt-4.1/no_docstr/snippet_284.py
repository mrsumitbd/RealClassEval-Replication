
import rasterio


class RIODataset:

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        self.rfile = rfile
        self.dataset = rasterio.open(rfile, 'r+')
        self.overviews = overviews
        self.overviews_resampling = overviews_resampling
        self.overviews_minsize = overviews_minsize

        if self.overviews is not None:
            for i in self.overviews:
                if i <= 1:
                    raise ValueError("Overview factors must be > 1")
            for idx in self.dataset.indexes:
                self.dataset.build_overviews(
                    self.overviews, resampling=self.overviews_resampling or rasterio.enums.Resampling.nearest)
            self.dataset.update_tags(
                ns='rio_overview', overviews=str(self.overviews))
        elif self.overviews_minsize is not None:
            # Build overviews automatically until the smallest dimension is less than overviews_minsize
            factors = []
            width, height = self.dataset.width, self.dataset.height
            minsize = min(width, height)
            factor = 2
            while minsize // factor >= self.overviews_minsize:
                factors.append(factor)
                factor *= 2
            if factors:
                for idx in self.dataset.indexes:
                    self.dataset.build_overviews(
                        factors, resampling=self.overviews_resampling or rasterio.enums.Resampling.nearest)
                self.dataset.update_tags(
                    ns='rio_overview', overviews=str(factors))

    def __setitem__(self, key, item):
        # key: (band, window) or band
        if isinstance(key, tuple):
            band, window = key
            self.dataset.write(item, band, window=window)
        else:
            band = key
            self.dataset.write(item, band)

    def close(self):
        if self.dataset:
            self.dataset.close()
            self.dataset = None
