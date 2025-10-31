
class RIODataset:

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):

        self.rfile = rfile
        self.overviews = overviews
        self.overviews_resampling = overviews_resampling
        self.overviews_minsize = overviews_minsize

    def __setitem__(self, key, item):

        setattr(self, key, item)

    def close(self):

        if hasattr(self, 'rfile'):
            self.rfile.close()
