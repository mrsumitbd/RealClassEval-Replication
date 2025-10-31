
class RIODataset:

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        self.rfile = rfile
        self.overviews = overviews
        self.overviews_resampling = overviews_resampling
        self.overviews_minsize = overviews_minsize
        self.dataset = self._open_dataset()

    def _open_dataset(self):
        import rasterio
        return rasterio.open(self.rfile)

    def __setitem__(self, key, item):
        with rasterio.open(self.rfile, 'r+') as dst:
            dst.write(item, key)

    def close(self):
        self.dataset.close()
