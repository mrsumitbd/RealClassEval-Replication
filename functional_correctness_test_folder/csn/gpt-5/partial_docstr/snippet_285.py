class RIOTag:

    def __init__(self, rfile, name):
        '''Init the rasterio tag.'''
        try:
            import rasterio
        except ImportError as e:
            raise ImportError("rasterio is required to use RIOTag") from e
        self._rio = rasterio
        self._path = rfile
        self._ns = name if name is not None else None
        self._ds = self._rio.open(self._path, mode='r+')

    def __setitem__(self, key, item):
        if self._ds is None:
            raise RuntimeError("Dataset is closed.")
        if not isinstance(key, str):
            key = str(key)
        value = item if isinstance(item, str) else str(item)
        if self._ns:
            self._ds.update_tags(ns=self._ns, **{key: value})
        else:
            self._ds.update_tags(**{key: value})

    def close(self):
        '''Close the file.'''
        if self._ds is not None:
            try:
                self._ds.close()
            finally:
                self._ds = None
