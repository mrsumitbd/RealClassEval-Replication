import numpy as np


class RIOTag:
    '''Rasterio wrapper to allow da.store on tag.'''

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        '''Put the data in the tag.'''
        if hasattr(item, "compute"):
            item = item.compute()
        arr = np.asarray(item)
        if arr.size == 1:
            value = arr.reshape(-1)[0]
        else:
            value = arr.tolist()
        self.rfile.update_tags(**{self.name: str(value)})

    def close(self):
        '''Close the file.'''
        try:
            self.rfile.close()
        except Exception:
            pass
