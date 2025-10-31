import rasterio
import numpy as np
from rasterio.enums import Resampling
from rasterio.windows import Window


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        self.path = rfile
        self._ds = None
        self._writable = False

        # Try to open writable, then fallback to read-only
        try:
            self._ds = rasterio.open(self.path, mode="r+")
            self._writable = True
        except Exception:
            self._ds = rasterio.open(self.path, mode="r")
            self._writable = False

        # Handle overviews if requested
        if overviews is not None:
            if not self._writable:
                # need writable to build overviews
                raise RuntimeError(
                    "Overviews requested but dataset is not writable (opened read-only).")

            if overviews_resampling is None:
                resampling = Resampling.nearest
            elif isinstance(overviews_resampling, Resampling):
                resampling = overviews_resampling
            else:
                # allow str like 'nearest', 'average', etc.
                resampling = Resampling[str(overviews_resampling).lower()]

            if overviews is True or str(overviews).lower() in ("auto",):
                min_dim = min(self._ds.width, self._ds.height)
                factors = []
                f = 2
                while min_dim // f >= int(overviews_minsize):
                    factors.append(f)
                    f *= 2
            elif isinstance(overviews, (list, tuple)):
                factors = [int(x) for x in overviews if int(x) > 1]
            else:
                raise ValueError(
                    "Invalid overviews parameter. Use True/'auto' or list of decimation factors.")

            if factors:
                self._ds.build_overviews(factors, resampling=resampling)
                # Optional: tag the dataset with overview information
                try:
                    self._ds.update_tags(ns="rio_overviews",
                                         factors=",".join(map(str, factors)),
                                         resampling=resampling.name)
                except Exception:
                    pass

    def __setitem__(self, key, item):
        # Writing requires writable dataset
        if not self._writable:
            raise RuntimeError(
                "Dataset is not writable. Opened in read-only mode.")

        ds = self._ds

        def _ensure_dtype(arr, indexes):
            if arr is None:
                return arr
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)

            # Normalize to (bands, ...) for dtype checking
            if arr.ndim == 2:
                bands = [indexes] if isinstance(
                    indexes, int) else list(indexes)
                target_dtypes = [ds.dtypes[b - 1] for b in bands]
                if len(set(target_dtypes)) == 1:
                    td = target_dtypes[0]
                    if arr.dtype.name != td:
                        arr = arr.astype(td, copy=False)
                return arr
            elif arr.ndim == 3:
                if isinstance(indexes, int):
                    target_dtypes = [ds.dtypes[indexes - 1]]
                else:
                    bands = list(indexes)
                    target_dtypes = [ds.dtypes[b - 1] for b in bands]
                # If all bands share same dtype, cast once
                if len(set(target_dtypes)) == 1:
                    td = target_dtypes[0]
                    if arr.dtype.name != td:
                        arr = arr.astype(td, copy=False)
                return arr
            else:
                return arr

        if isinstance(key, int):
            idx = int(key)
            arr = np.asarray(item)
            arr = _ensure_dtype(arr, idx)
            ds.write(arr, indexes=idx)
            return

        if isinstance(key, Window):
            win = key
            arr = np.asarray(item)
            if arr.ndim == 2:
                idxs = 1
            elif arr.ndim == 3:
                idxs = list(range(1, arr.shape[0] + 1))
            else:
                raise ValueError("Unsupported array shape for windowed write.")
            arr = _ensure_dtype(arr, idxs)
            ds.write(arr, indexes=idxs, window=win)
            return

        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError("Key tuple must be (indexes, window).")
            idxs, win = key
            if isinstance(win, tuple) and len(win) == 2 and all(isinstance(t, slice) for t in win):
                # Support numpy-like slicing ((rowslice, colslice))
                row_slice, col_slice = win
                row_start = 0 if row_slice.start is None else row_slice.start
                col_start = 0 if col_slice.start is None else col_slice.start
                row_stop = ds.height if row_slice.stop is None else row_slice.stop
                col_stop = ds.width if col_slice.stop is None else col_slice.stop
                height = row_stop - row_start
                width = col_stop - col_start
                win = Window(col_start, row_start, width, height)
            elif not isinstance(win, Window):
                raise ValueError(
                    "Window must be a rasterio.windows.Window or tuple of slices.")

            if isinstance(idxs, (list, tuple, np.ndarray)):
                idxs = [int(i) for i in idxs]
            elif isinstance(idxs, int):
                idxs = int(idxs)
            else:
                raise ValueError("Indexes must be int or sequence of ints.")

            arr = np.asarray(item)
            arr = _ensure_dtype(arr, idxs)
            ds.write(arr, indexes=idxs, window=win)
            return

        raise TypeError("Unsupported key type for __setitem__.")

    def close(self):
        '''Close the file.'''
        if self._ds is not None:
            try:
                self._ds.close()
            finally:
                self._ds = None
                self._writable = False
