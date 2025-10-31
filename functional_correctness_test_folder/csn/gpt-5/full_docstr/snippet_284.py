import rasterio
from rasterio.windows import Window, from_slices
from rasterio.enums import Resampling
from collections.abc import Iterable
import math
import os


class RIODataset:
    '''A wrapper for a rasterio dataset.'''

    def __init__(self, rfile, overviews=None, overviews_resampling=None, overviews_minsize=256):
        '''Init the rasterio dataset.'''
        if hasattr(rfile, "read") and hasattr(rfile, "write"):
            self.ds = rfile
            self._owns_ds = False
        else:
            mode = "r+"
            try:
                self.ds = rasterio.open(rfile, mode)
            except Exception:
                # fallback to read-only if not writable
                self.ds = rasterio.open(rfile, "r")
            self._owns_ds = True

        self._closed = False

        if overviews is None:
            overviews = self._auto_overview_factors(
                self.ds.width, self.ds.height, overviews_minsize)

        if overviews:
            resampling = self._parse_resampling(overviews_resampling)
            try:
                # build_overviews is a no-op if dataset is read-only; guard with try
                self.ds.build_overviews(overviews, resampling)
                # Some drivers (e.g., GTiff) may store resampling in metadata
                try:
                    self.ds.update_tags(ns='rio_overview', resampling=str(
                        resampling).split('.')[-1])
                except Exception:
                    pass
            except Exception:
                # Ignore overview building errors on unsupported drivers/modes
                pass

    def __setitem__(self, key, item):
        '''Put the data chunk in the image.'''
        if self._closed:
            raise RuntimeError("Dataset is closed")

        window = None
        indexes = None

        if isinstance(key, Window):
            window = key
        elif isinstance(key, tuple):
            # Possible forms:
            # (row_slice, col_slice)
            # (indexes, row_slice, col_slice)
            if len(key) == 2:
                row_slice, col_slice = key
                window = from_slices(row_slice, col_slice,
                                     height=self.ds.height, width=self.ds.width)
            elif len(key) == 3:
                idx, row_slice, col_slice = key
                indexes = idx
                window = from_slices(row_slice, col_slice,
                                     height=self.ds.height, width=self.ds.width)
            else:
                raise ValueError(
                    "Invalid key. Expected (row_slice, col_slice) or (indexes, row_slice, col_slice).")
        else:
            raise TypeError(
                "Key must be a rasterio.windows.Window or a tuple of slices.")

        if isinstance(indexes, Iterable) and not isinstance(indexes, (list, tuple)):
            indexes = list(indexes)

        # Normalize indexes: None, int, or list of ints
        if indexes is not None:
            if isinstance(indexes, int):
                pass
            elif isinstance(indexes, (list, tuple)):
                if not all(isinstance(i, int) for i in indexes):
                    raise TypeError("Indexes must be int or iterable of ints.")
            else:
                raise TypeError("Indexes must be int or iterable of ints.")

        self.ds.write(item, window=window, indexes=indexes)

    def close(self):
        '''Close the file.'''
        if not self._closed and self._owns_ds:
            try:
                self.ds.close()
            finally:
                self._closed = True

    @staticmethod
    def _parse_resampling(resampling):
        if resampling is None:
            return Resampling.average
        if isinstance(resampling, Resampling):
            return resampling
        if isinstance(resampling, str):
            key = resampling.strip().lower()
            for r in Resampling:
                if r.name.lower() == key:
                    return r
        raise ValueError("Invalid resampling value.")

    @staticmethod
    def _auto_overview_factors(width, height, minsize):
        if minsize is None or minsize <= 0:
            return []
        min_dim = min(width, height)
        if min_dim <= minsize:
            return []
        factors = []
        f = 2
        while min_dim / f >= minsize:
            factors.append(f)
            f *= 2
        return factors
